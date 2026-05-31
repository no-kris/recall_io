from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi_betterauth import BetterAuth
from fastapi_betterauth import User as BetterAuthUser
from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import config
from app.core.database import db
from app.models.user import User
from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository

_model = None
_better_auth = BetterAuth(base_url=config.NEON_AUTH)


def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


async def generate_embeddings(title: str, content: str) -> list[float]:
    model = get_model()

    combined_text = f"{title} {content}"

    embedding = model.encode(combined_text).tolist()

    return embedding


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_db_session() as session:
        yield session


async def get_user_service(session: AsyncSession = Depends(get_db)):
    """Provide a UserService with injected repository."""
    from app.services.user_service import UserService

    repository = UserRepository(session)
    return UserService(repository)


async def get_note_service(session: AsyncSession = Depends(get_db)):
    """Provide a NoteService with injected repository."""
    from app.services.note_service import NoteService

    repository = NoteRepository(session)
    return NoteService(repository)


async def get_current_user(
    better_auth_user: BetterAuthUser = Depends(_better_auth),
    session: AsyncSession = Depends(get_db),
) -> User:
    """
    Get the current authenticated user.
    Uses better auth to validate the JWT token from the Neon Auth table.
    """
    auth_provider_id = better_auth_user.get("sub")

    if not auth_provider_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    repository = UserRepository(session)
    user = await repository.get_user_by_auth_provider_id(auth_provider_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
