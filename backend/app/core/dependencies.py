from typing import AsyncGenerator

from sentence_transformers import SentenceTransformer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db

_model = None


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
