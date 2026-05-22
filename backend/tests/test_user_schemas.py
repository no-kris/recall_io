import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserPublic, UserUpdate


class MockUser:
    def __init__(self, id: int, username: str, email: str, notes_count: int):
        self.id = id
        self.username = username
        self.email = email
        self.notes_count = notes_count


def test_user_public_notes_count_mapping():

    mock = MockUser(id=1, username="testuser", email="test@example.com", notes_count=14)

    public_user = UserPublic.model_validate(mock)

    assert public_user.id == 1
    assert public_user.username == "testuser"
    assert public_user.email == "test@example.com"
    assert public_user.notes_count == 14


@pytest.mark.parametrize(
    "invalid_email",
    ["plainaddress", "@missinguser.com", "user@.com", "user@domain", " "],
)
def test_invalid_email_validation(invalid_email):
    with pytest.raises(ValidationError):
        UserCreate(username="testuser", email=invalid_email, auth_provider_id="id")


@pytest.mark.parametrize(
    "username, expected_fail",
    [
        ("abc", False),  # Min length 3 (valid)
        ("ab", True),  # Min length 3 (invalid)
        ("a" * 50, False),  # Max length 50 (valid)
        ("a" * 51, True),  # Max length 50 (invalid)
        (None, False),  # Optional field (valid)
    ],
)
def test_user_update_username_validation(username, expected_fail):
    if expected_fail:
        with pytest.raises(ValidationError):
            UserUpdate(username=username)
    else:
        user_update = UserUpdate(username=username)
        assert user_update.username == username
