from uuid import UUID

from pydantic import BaseModel, Field


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl_seconds: int | None = Field(default=None, ge=5 * 60)


class SecretKeyGet(BaseModel):
    secret_key: UUID


class SecretGet(BaseModel):
    secret: str
