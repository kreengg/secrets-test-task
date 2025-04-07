from fastapi import APIRouter

from src.api.dependencies import SessionDep
from src.schemas.secret import SecretCreate, SecretKeyGet

router = APIRouter(
    prefix="/secret",
    tags=["Secrets"],
)


@router.post("")
async def create_secret(session: SessionDep, secret: SecretCreate) -> SecretKeyGet: ...
