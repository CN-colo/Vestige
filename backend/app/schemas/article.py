from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str
    cover_image: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    cover_image: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None


class ArticleResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool
    published_at: Optional[datetime] = None
    view_count: int
    like_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None
    author: Optional[dict] = None  # {"id": x, "username": "xxx", "avatar": "xxx"}

    class Config:
        from_attributes = True

    @field_validator('author', mode='before')
    @classmethod
    def convert_user_to_dict(cls, v: Any) -> Optional[dict]:
        """Convert User ORM object to dict for serialization."""
        if v is None:
            return None
        if isinstance(v, dict):
            return v
        # Assume it's a User ORM object
        return {
            "id": v.id,
            "username": v.username,
            "avatar": getattr(v, 'avatar', None)
        }


class ArticleListResponse(BaseModel):
    id: int
    title: str
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool
    published_at: Optional[datetime] = None
    view_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ArticlePublicResponse(BaseModel):
    id: int
    title: str
    content: str
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    view_count: int
    author: Optional[dict] = None  # {"id": x, "username": "xxx"}

    class Config:
        from_attributes = True