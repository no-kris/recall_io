import pytest
from sqlalchemy import text

from app.core.database import db


@pytest.mark.asyncio
async def test_db_connection_ping():
    """
    Ping the database to see if a connection can be made.
    """
    async with db.get_db_session() as session:
        result = await session.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1
