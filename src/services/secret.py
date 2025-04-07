from uuid import UUID

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.log import Action, Log
from src.models.secret import Secret
from src.schemas.secret import SecretCreate
from src.utils.secret import encode_secret


class SecretService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_secret(self, request: Request, secret_data: SecretCreate) -> UUID:
        secret = Secret(
            secret=encode_secret(secret_data.secret),
            passphrase=secret_data.passphrase,
            ttl_seconds=secret_data.ttl_seconds,
        )
        self.session.add(secret)
        await self.session.flush()
        await self.session.refresh(secret)

        log = Log(
            secret_key=secret.secret_key,
            action=Action.create,
            ip_address=request.client.host,
            ttl_seconds=secret.ttl_seconds,
        )
        self.session.add(log)
        await self.session.commit()

        return secret.secret_key
