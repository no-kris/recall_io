from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Return a user that matches the passed in user id.
        """
        return await self.session.get(User, user_id)

    async def get_user_by_auth_provider_id(
        self, auth_provider_id: str
    ) -> Optional[User]:
        """
        Find and return a user by their auth provider ID.
        Used during login/authorization to identify the user from the auth system.
        """
        q = select(User).where(User.auth_provider_id == auth_provider_id)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Find and return a user whose email matches the passed in email.
        """
        q = select(User).where(User.email == email)
        result = await self.session.execute(q)
        return result.scalars().first()

    async def add(self, user: User) -> User:
        """
        Add a new user to the database.
        """
        self.session.add(user)
        await self.session.flush()
        return user

    async def update(self, user: User, **fields) -> User:
        """
        Update user in database with the passed in user fields.
        """
        for k, v in fields.items():
            setattr(user, k, v)
        await self.session.flush()
        return user

    async def delete(self, user: User) -> None:
        """
        Delete a user from the database.
        """
        await self.session.delete(user)
        await self.session.flush()
