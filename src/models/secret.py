from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Secret(Base):
    __tablename__ = "secret"

    secret_key: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    secret: Mapped[bytes] = mapped_column(nullable=False)
    passphrase: Mapped[str | None] = mapped_column(nullable=True)
    ttl_seconds: Mapped[int | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        nullable=False,
    )
