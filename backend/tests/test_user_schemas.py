import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate


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
