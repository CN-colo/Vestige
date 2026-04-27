from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ApiKeyBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permissions: Optional[List[str]] = None  # ["read:public", "write:public"]
    expires_at: Optional[datetime] = None


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKeyUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    permissions: Optional[List[str]] = None
    is_active: Optional[bool] = None


class ApiKeyResponse(BaseModel):
    id: int
    name: Optional[str] = None
    permissions: Optional[List[str]] = None
    is_active: bool
    last_used_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    created_at: datetime
    # Note: actual key is only shown once when created

    class Config:
        from_attributes = True


class ApiKeyCreatedResponse(BaseModel):
    id: int
    key: str  # Full key shown only on creation
    name: Optional[str] = None
    permissions: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True