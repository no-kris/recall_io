from datetime import datetime

from sqlalchemy import String, func, select
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from app.models.base import Base
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
    notes_count: Mapped[int] = column_property(
        select(func.count(Note.id)).where(Note.author_id == id).scalar_subquery()
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
