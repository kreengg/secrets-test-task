import datetime
from uuid import UUID

from fastapi import Request
from redis import Redis
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.log import Action, Log
from src.models.secret import Secret
from src.schemas.secret import SecretCreate
from src.utils.secret import decode_secret, encode_secret


class SecretService:
    def __init__(self, session: AsyncSession, cache: Redis):
        self.session = session
        self.cache = cache

    async def create_secret(self, request: Request, secret_data: SecretCreate) -> UUID:
        # TODO: вынести логику бд и кеша в отдельные методы, но пока нет идей как

        secret = Secret(
            secret=encode_secret(secret_data.secret),
            passphrase=secret_data.passphrase,  # Надо ли шифровать passphrase?
            ttl_seconds=secret_data.ttl_seconds,
        )
        self.session.add(secret)
        await self.session.flush()
        await self.session.refresh(secret)

        self.cache.hset(
            str(secret.secret_key).encode(),
            mapping={
                "secret": secret.secret,
                "passphrase": secret.passphrase,
                "ttl_seconds": secret.ttl_seconds,
                "created_at": secret.created_at.timestamp(),
            },
        )

        self._log_secret_action(Action.create, request, secret)

        await self.session.commit()

        return secret.secret_key

    async def get_secret(self, request: Request, secret_key: UUID) -> str | None:
        # TODO: вынести логику бд и кеша в отдельные методы, но пока нет идей как
        secret_data = self.cache.hgetall(
            str(secret_key).encode(),
        )

        if secret_data:
            secret = Secret(
                secret_key=secret_key,
                secret=secret_data["secret"],
                passphrase=secret_data["passphrase"],
                ttl_seconds=int(secret_data["ttl_seconds"]),
                created_at=datetime.datetime.fromtimestamp(
                    float(secret_data["created_at"]), datetime.UTC
                ),
            )
        else:
            stmt = select(Secret).where(Secret.secret_key == secret_key)
            result = await self.session.execute(stmt)
            secret = result.scalars().first()
        if not secret:
            return None

        self.cache.delete(str(secret_key).encode())
        delete_stmt = delete(Secret).where(Secret.secret_key == secret_key)
        await self.session.execute(delete_stmt)

        if not self._isSecretAlive(secret.created_at, secret.ttl_seconds):
            return None

        encoded_secret = secret.secret
        self._log_secret_action(Action.get, request, secret)

        await self.session.commit()

        decoded_secret = decode_secret(encoded_secret)
        return decoded_secret

    async def delete_secret(self, request: Request, secret_key: UUID) -> None:
        # TODO: вынести логику бд и кеша в отдельные методы, но пока нет идей как

        stmt = select(Secret).where(Secret.secret_key == secret_key)
        result = await self.session.execute(stmt)
        secret = result.scalars().first()
        if not secret:
            return None

        self.cache.delete(str(secret_key).encode())
        await self.session.delete(secret)

        self._log_secret_action(Action.delete, request, secret)

        await self.session.commit()

    def _log_secret_action(
        self, action: Action, request: Request, secret: Secret
    ) -> None:
        log = Log(
            secret_key=secret.secret_key,
            action=action,
            ip_address=request.client.host,
            ttl_seconds=secret.ttl_seconds,
        )
        self.session.add(log)

    def _isSecretAlive(self, created_at: datetime.datetime, ttl_seconds: int | None):
        if not ttl_seconds:
            return True

        secret_unavaliable_at = created_at + datetime.timedelta(seconds=ttl_seconds)

        return secret_unavaliable_at > datetime.datetime.now(datetime.UTC)
