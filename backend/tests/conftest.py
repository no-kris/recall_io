import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.models.base import Base
from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserRepository


@pytest.fixture
async def test_engine():
    """
    In-memory SQLite engine for testing.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
async def test_db_session(test_engine):
    """
    Mock database session for testing.
    """
    async_session = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session


@pytest.fixture
async def user_repository(test_db_session):
    """Provide a UserRepository with the test database session."""
    return UserRepository(test_db_session)


@pytest.fixture
async def note_repository(test_db_session):
    """Provide a NoteRepository with the test database session."""
    return NoteRepository(test_db_session)
