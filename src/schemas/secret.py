from pydantic import BaseModel, Field


class SecretCreate(BaseModel):
    secret: str
    passphrase: str | None = None
    ttl: int | None = Field(default=None, gt=0)


class SecretKeyGet(BaseModel):
    secret_key: str


class SecretGet(BaseModel):
    secret: str
