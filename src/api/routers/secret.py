from fastapi import APIRouter, Request

from src.api.dependencies import SessionDep
from src.schemas.secret import SecretCreate, SecretKeyGet
from src.services.secret import SecretService

router = APIRouter(
    prefix="/secret",
    tags=["Secrets"],
)


@router.post("")
async def create_secret(
    session: SessionDep,
    request: Request,
    secret: SecretCreate,
) -> SecretKeyGet:
    service = SecretService(session)
    secret_key = await service.create_secret(request, secret)

    return SecretKeyGet(secret_key=secret_key)
