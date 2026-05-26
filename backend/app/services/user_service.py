from app.core.exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def authenticate_user(self, auth_provider_id: str) -> User:
        """
        Find user by auth_provider_id.
        Called after Neon Auth validates user credentials.
        """
        user = await self.repository.get_user_by_auth_provider_id(auth_provider_id)
        if not user:
            raise UserNotFoundError("User not found.")
        if not user.is_active:
            raise UserNotFoundError("User account is inactive.")
        return user

    async def create_user(
        self, auth_provider_id: str, email: str, username: str
    ) -> User:
        """
        Create a new user after Neon auth sign up.
        Raises UserAlreadyExistsError if user record already exists.
        """
        existing_user = await self.repository.get_user_by_auth_provider_id(
            auth_provider_id
        )
        if existing_user:
            raise UserAlreadyExistsError(f"{username} already exists.")

        user = User(auth_provider_id=auth_provider_id, email=email, username=username)
        return await self.repository.add(user)

    async def update_user_profile(self, user_id: int, **fields) -> User:
        """
        Update user profile information.
        Raises UserNotFoundError if user doesn't exist.
        """
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("Could not update user. User not found.")

        return await self.repository.update(user, **fields)

    async def delete_user_account(self, user_id: int) -> None:
        """
        Delete a user account.
        Raises UserNotFoundError if user doesn't exist.
        """
        user = await self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(
                "Could not delete account because the account was not found."
            )

        await self.repository.delete(user)
