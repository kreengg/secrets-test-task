from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import config

SQLALCHEMY_DATABASE_URL = config.db.url()
DATABASE_PARAMS = {
    "echo": config.db.echo,
}

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    **DATABASE_PARAMS,
)


class Base(DeclarativeBase):
    pass


async_session_maker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    async with async_session_maker() as session:
        yield session
