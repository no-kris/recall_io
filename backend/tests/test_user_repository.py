import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_get_user_by_id(
    user_repository: UserRepository, test_db_session: AsyncSession
):
    user = User(
        id=1, username="john", email="john@example.com", auth_provider_id="auth_123"
    )
    test_db_session.add(user)
    await test_db_session.flush()

    result = await user_repository.get_user_by_id(user.id)

    assert result is not None
    assert result.email == "john@example.com"
    assert result.username == "john"
    assert result.auth_provider_id == "auth_123"


@pytest.mark.asyncio
async def test_get_user_by_auth_id(
    user_repository: UserRepository, test_db_session: AsyncSession
):
    user = User(
        id=5, username="chloe", email="chloe@example.com", auth_provider_id="auth_765"
    )
    test_db_session.add(user)
    await test_db_session.flush()

    result = await user_repository.get_user_by_id(user.id)

    assert result is not None
    assert result.auth_provider_id == "auth_765"


@pytest.mark.asyncio
async def test_get_user_by_email(
    user_repository: UserRepository, test_db_session: AsyncSession
):
    user = User(username="jane", email="jane@example.com", auth_provider_id="auth_456")
    test_db_session.add(user)
    await test_db_session.flush()
    result = await user_repository.get_user_by_email(user.email)
    assert result is not None
    assert result.username == "jane"
    assert result.email == "jane@example.com"
    assert result.auth_provider_id == "auth_456"


@pytest.mark.asyncio
async def test_update_user(
    user_repository: UserRepository, test_db_session: AsyncSession
):
    user = User(
        id=3, username="alice", email="alice@example.com", auth_provider_id="auth_000"
    )
    test_db_session.add(user)
    await test_db_session.flush()

    updated = await user_repository.update(user, username="alice_updated")

    assert updated.username == "alice_updated"
    assert updated.email == "alice@example.com"


@pytest.mark.asyncio
async def test_delete_user(
    user_repository: UserRepository, test_db_session: AsyncSession
):
    user = User(
        id=4, username="bob", email="bob@example.com", auth_provider_id="auth_012"
    )
    test_db_session.add(user)
    await test_db_session.flush()

    result = await user_repository.get_user_by_id(user.id)

    assert result is not None

    await user_repository.delete(user)

    deleted_user = await user_repository.get_user_by_id(user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_get_nonexistent_user(user_repository: UserRepository) -> None:
    """Test that getting a nonexistent user returns None."""
    result = await user_repository.get_user_by_id(999)
    assert result is None
