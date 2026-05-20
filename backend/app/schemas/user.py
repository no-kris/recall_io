from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    auth_provider_id: str


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None


class UserPublic(BaseModel):
    """
    Public api facing schema.
    """

    id: int
    username: str
    email: EmailStr
    notes_count: int

    model_config = ConfigDict(from_attributes=True)
