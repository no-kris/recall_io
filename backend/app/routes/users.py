import os

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_db, get_user_service
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic, UserUpdate
from app.services.user_service import UserService

ENVIRONMENT = os.getenv("ENVIRONMENT")

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserPublic)
async def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user's profile.
    """
    return current_user


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db),
):
    """
    Create and store a user in the database.
    """
    try:
        user = await service.create_user(
            auth_provider_id=user_data.auth_provider_id,
            email=user_data.email,
            username=user_data.username,
        )
        await session.commit()
        return user
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=UserPublic)
async def login(
    auth_provider_id: str,
    service: UserService = Depends(get_user_service),
):
    """
    Authenticate and login the user.
    """
    try:
        user = await service.authenticate_user(auth_provider_id=auth_provider_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{user_id}", response_model=UserPublic)
async def update_profile(
    user_id: int,
    user_update: UserUpdate,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update user profile.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        user = await service.update_user_profile(
            user_id, **user_update.model_dump(exclude_none=True)
        )
        await session.commit()
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete user from database.
    """
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    try:
        await service.delete_user_account(user_id)
        await session.commit()
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


if ENVIRONMENT == "development":
    """
    API Routes for testing/debugging purposes only.
    """

    @router.get("/{user_id}/debug", tags=["DEBUG ONLY"])
    async def get_user(user_id: int, session: AsyncSession = Depends(get_db)):
        """
        DEBUG ROUTE - DEVELOPMENT ONLY
        This route reveals all user data. Only available in development mode.
        """
        from app.repositories.user_repository import UserRepository

        repository = UserRepository(session)
        try:
            user = await repository.get_user_by_id(user_id)
            return user
        except UserNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
