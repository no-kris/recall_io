from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.note import Note


class User(Base):
    """
    Database table definitions for users table.
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    auth_provider_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    notes: Mapped[list["Note"]] = relationship(back_populates="author")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


# Late import to prevent runtime circular dependencies
from app.models.note import Note  # noqa

User.notes_count = column_property(
    select(func.count(Note.id))
    .where(Note.author_id == User.id)
    .scalar_subquery()
)
