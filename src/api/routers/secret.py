from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from src.api.dependencies import SessionDep
from src.api.schemas import ErrorResponse, StatusResponse
from src.schemas.secret import SecretCreate, SecretGet, SecretKeyGet
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


# Если следовать стандартам HTTP, метод GET должен быть идемпотентным,
# а значит возвращать одинаковый результат,
# и не выполнять никакую логику на стороне сервера.
# Но по тз мы будем удалять секрет (или скрывать), что по идее не совсем правильно
@router.get(
    "/{secret_key}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
    },
)
async def get_secret(
    session: SessionDep,
    request: Request,
    secret_key: UUID,
) -> SecretGet:
    service = SecretService(session)
    secret = await service.get_secret(request, secret_key)
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Secret not found"
        )

    return SecretGet(secret=secret)


@router.delete(
    "/{secret_key}",
)
async def delete_secret(
    session: SessionDep,
    request: Request,
    secret_key: UUID,
) -> StatusResponse:
    service = SecretService(session)
    await service.delete_secret(request, secret_key)
    # Нужна ли ошибка если по ключу ничего не найдено?

    return StatusResponse(status="secret_deleted")
