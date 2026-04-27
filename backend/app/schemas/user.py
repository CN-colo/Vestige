from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    contact: Optional[str] = Field(None, max_length=100)
    card_enabled: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    contact: Optional[str] = None
    card_enabled: bool = True
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPublic(BaseModel):
    id: int
    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    contact: Optional[str] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None