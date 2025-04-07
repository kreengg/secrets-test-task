from uuid import UUID

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.log import Action, Log
from src.models.secret import Secret
from src.schemas.secret import SecretCreate
from src.utils.secret import decode_secret, encode_secret


class SecretService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_secret(self, request: Request, secret_data: SecretCreate) -> UUID:
        # TODO: кеш

        secret = Secret(
            secret=encode_secret(secret_data.secret),
            passphrase=secret_data.passphrase,
            ttl_seconds=secret_data.ttl_seconds,
        )
        self.session.add(secret)
        await self.session.flush()
        await self.session.refresh(secret)

        self._log_secret_action(Action.create, request, secret)

        await self.session.commit()

        return secret.secret_key

    async def get_secret(self, request: Request, secret_key: UUID) -> str | None:
        # TODO: кеш
        # TODO: проверка ttl секрета

        stmt = select(Secret).where(Secret.secret_key == secret_key)
        result = await self.session.execute(stmt)
        secret = result.scalars().first()
        if not secret:
            return None
        encoded_secret = secret.secret

        self._log_secret_action(Action.get, request, secret)
        self._log_secret_action(Action.delete, request, secret)

        await self.session.delete(secret)
        await self.session.commit()

        decoded_secret = decode_secret(encoded_secret)
        return decoded_secret

    async def delete_secret(self, request: Request, secret_key: UUID) -> None:
        stmt = select(Secret).where(Secret.secret_key == secret_key)
        result = await self.session.execute(stmt)
        secret = result.scalars().first()
        if not secret:
            return None
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
