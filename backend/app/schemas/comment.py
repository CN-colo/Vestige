from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentCreate(CommentBase):
    content_type: str = Field(..., pattern="^(article|project)$")
    content_id: int
    parent_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentAuthorResponse(BaseModel):
    id: int
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True


class CommentResponse(BaseModel):
    id: int
    user_id: int
    content_type: str
    content_id: int
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[CommentAuthorResponse] = None
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True


class CommentListResponse(BaseModel):
    id: int
    user_id: int
    content: str
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[CommentAuthorResponse] = None

    class Config:
        from_attributes = True


# Resolve forward reference
CommentResponse.model_rebuild()