from typing import AsyncGenerator

from database import db
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_db_session() as session:
        yield session
