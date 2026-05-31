import pytest
from httpx import ASGITransport, AsyncClient

from app.core.dependencies import get_db
from app.main import app
from app.models.user import User


@pytest.fixture
def override_get_db(test_db_session):
    """Override the get_db dependency to use test database."""

    async def _get_db():
        return test_db_session

    return _get_db


@pytest.mark.asyncio
async def test_signup_success(override_get_db, test_db_session):
    """Test successful user signup."""
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/users/signup",
            json={
                "auth_provider_id": "auth_123",
                "email": "newuser@example.com",
                "username": "newuser",
            },
        )

    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"

    # Cleanup
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_signup_user_already_exists(override_get_db, test_db_session):
    """Test signup fails when user already exists."""
    app.dependency_overrides[get_db] = override_get_db

    # Create existing user
    user = User(
        auth_provider_id="auth_123", email="existing@example.com", username="existing"
    )
    test_db_session.add(user)
    await test_db_session.flush()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/users/signup",
            json={
                "auth_provider_id": "auth_123",
                "email": "existing@example.com",
                "username": "existing",
            },
        )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_success(override_get_db, test_db_session):
    """Test successful login."""
    app.dependency_overrides[get_db] = override_get_db

    # Create user first
    user = User(
        auth_provider_id="auth_123", email="test@example.com", username="testuser"
    )
    test_db_session.add(user)
    await test_db_session.flush()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/users/login", params={"auth_provider_id": "auth_123"}
        )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_login_user_not_found(override_get_db):
    """Test login fails when user doesn't exist."""
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/users/login", params={"auth_provider_id": "nonexistent"}
        )

    assert response.status_code == 404

    app.dependency_overrides.clear()
