from datetime import UTC, datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Action(Enum):
    create = "create"
    get = "get"
    delete = "delete"


class Log(Base):
    __tablename__ = "log"

    # Возможно не стоит удалять секреты из бд, после получения/удаления,
    # но тогда все равно не получится сделать Foreign Key в логи,
    # т.к. их надо очищать с периодичностью, поэтому secret_key в логах не FK

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, unique=True)
    secret_key: Mapped[UUID] = mapped_column(nullable=False)
    action: Mapped["Action"] = mapped_column(nullable=False)
    ip_address: Mapped[str] = mapped_column(nullable=False)
    ttl_seconds: Mapped[int | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )
