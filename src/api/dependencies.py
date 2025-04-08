from typing import Annotated

import redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database import get_session
from src.infra.redis import get_redis_client

# TODO - объединить в одну сущность инфраструктуры
DbSessionDep = Annotated[AsyncSession, Depends(get_session)]

RedisDep = Annotated[redis.Redis, Depends(get_redis_client)]
