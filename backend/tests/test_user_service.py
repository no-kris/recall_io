# File: study-vault/backend/tests/test_user_service.py

from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models.user import User
from app.services.user_service import UserService


@pytest.fixture
def mock_user_repository():
    """Create a mock UserRepository."""
    mock = AsyncMock()
    return mock


@pytest.mark.asyncio
async def test_create_user_raises_error_if_already_exists(mock_user_repository):
    """Test that creating a user with existing auth_provider_id raises UserAlreadyExistsError."""
    # Setup: Mock repository to return an existing user
    existing_user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="testuser",
    )
    mock_user_repository.get_user_by_auth_provider_id.return_value = existing_user

    service = UserService(mock_user_repository)

    # Test & Assert
    with pytest.raises(UserAlreadyExistsError):
        await service.create_user("auth_123", "test@example.com", "testuser")


@pytest.mark.asyncio
async def test_create_user_success(mock_user_repository):
    """Test successfully creating a new user."""
    # Setup: Mock repository to return None (user doesn't exist), then return the created user
    mock_user_repository.get_user_by_auth_provider_id.return_value = None
    new_user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="testuser",
    )
    mock_user_repository.add.return_value = new_user

    service = UserService(mock_user_repository)

    # Test
    result = await service.create_user("auth_123", "test@example.com", "testuser")

    # Assert
    assert result == new_user
    assert result.auth_provider_id == "auth_123"
    assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_authenticate_user_raises_error_if_not_found(mock_user_repository):
    """Test that authenticating a non-existent user raises UserNotFoundError."""
    # Setup: Mock repository to return None
    mock_user_repository.get_user_by_auth_provider_id.return_value = None

    service = UserService(mock_user_repository)

    # Test & Assert
    with pytest.raises(UserNotFoundError):
        await service.authenticate_user("non_existent_auth_id")


@pytest.mark.asyncio
async def test_authenticate_user_raises_error_if_inactive(mock_user_repository):
    """Test that authenticating an inactive user raises UserNotFoundError."""
    # Setup: Mock repository to return an inactive user
    inactive_user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="testuser",
        is_active=False,
    )
    mock_user_repository.get_user_by_auth_provider_id.return_value = inactive_user

    service = UserService(mock_user_repository)

    # Test & Assert
    with pytest.raises(UserNotFoundError):
        await service.authenticate_user("auth_123")


@pytest.mark.asyncio
async def test_authenticate_user_success(mock_user_repository):
    """Test successfully authenticating a user."""
    # Setup: Mock repository to return an active user
    active_user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="testuser",
        is_active=True,
    )
    mock_user_repository.get_user_by_auth_provider_id.return_value = active_user

    service = UserService(mock_user_repository)

    # Test
    result = await service.authenticate_user("auth_123")

    # Assert
    assert result == active_user
    assert result.is_active is True


@pytest.mark.asyncio
async def test_update_user_profile_raises_error_if_not_found(mock_user_repository):
    """Test that updating a non-existent user raises UserNotFoundError."""
    # Setup: Mock repository to return None
    mock_user_repository.get_user_by_id.return_value = None

    service = UserService(mock_user_repository)

    # Test & Assert
    with pytest.raises(UserNotFoundError):
        await service.update_user_profile(999, username="newname")


@pytest.mark.asyncio
async def test_update_user_profile_success(mock_user_repository):
    """Test successfully updating a user profile."""
    # Setup: Mock repository to return a user, then return updated user
    user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="oldname",
    )
    updated_user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="newname",
    )
    mock_user_repository.get_user_by_id.return_value = user
    mock_user_repository.update.return_value = updated_user

    service = UserService(mock_user_repository)

    # Test
    result = await service.update_user_profile(1, username="newname")

    # Assert
    assert result == updated_user
    assert result.username == "newname"


@pytest.mark.asyncio
async def test_delete_user_account_raises_error_if_not_found(mock_user_repository):
    """Test that deleting a non-existent user raises UserNotFoundError."""
    # Setup: Mock repository to return None
    mock_user_repository.get_user_by_id.return_value = None

    service = UserService(mock_user_repository)

    # Test & Assert
    with pytest.raises(UserNotFoundError):
        await service.delete_user_account(999)


@pytest.mark.asyncio
async def test_delete_user_account_success(mock_user_repository):
    """Test successfully deleting a user account."""
    # Setup: Mock repository to return a user
    user = User(
        id=1,
        auth_provider_id="auth_123",
        email="test@example.com",
        username="testuser",
    )
    mock_user_repository.get_user_by_id.return_value = user

    service = UserService(mock_user_repository)

    # Test
    await service.delete_user_account(1)

    # Assert: Verify delete was called
    mock_user_repository.delete.assert_called_once_with(user)
