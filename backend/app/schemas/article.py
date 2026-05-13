from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime

# HTML content max size: 500KB
MAX_HTML_CONTENT_SIZE = 524288


class ArticleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    content_type: Optional[str] = Field(default="markdown")
    cover_image: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v: Optional[str]) -> str:
        """Validate content_type is either 'markdown' or 'html'."""
        if v is None:
            return "markdown"
        if v not in ['markdown', 'html']:
            raise ValueError('content_type must be "markdown" or "html"')
        return v

    @field_validator('content')
    @classmethod
    def validate_content_size(cls, v: str, info) -> str:
        """Validate HTML content size does not exceed 500KB."""
        # Check if content_type is html (from validation info)
        content_type = info.data.get('content_type', 'markdown')
        if content_type == 'html' and len(v.encode('utf-8')) > MAX_HTML_CONTENT_SIZE:
            raise ValueError(f'HTML content exceeds {MAX_HTML_CONTENT_SIZE} bytes (500KB) limit')
        return v


class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    content_type: Optional[str] = None
    cover_image: Optional[str] = None
    summary: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    is_public: Optional[bool] = None

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v: Optional[str]) -> Optional[str]:
        """Validate content_type is either 'markdown' or 'html'."""
        if v is None:
            return None
        if v not in ['markdown', 'html']:
            raise ValueError('content_type must be "markdown" or "html"')
        return v

    @field_validator('content')
    @classmethod
    def validate_content_size(cls, v: Optional[str], info) -> Optional[str]:
        """Validate HTML content size does not exceed 500KB."""
        if v is None:
            return None
        content_type = info.data.get('content_type')
        if content_type == 'html' and len(v.encode('utf-8')) > MAX_HTML_CONTENT_SIZE:
            raise ValueError(f'HTML content exceeds {MAX_HTML_CONTENT_SIZE} bytes (500KB) limit')
        return v


class ArticleResponse(BaseModel):
    id: int
    user_id: int
    title: str
    content: str
    content_type: str = "markdown"
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
    content_type: str = "markdown"
    cover_image: Optional[str] = None
    summary: Optional[str] = None
    tags: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    view_count: int
    author: Optional[dict] = None  # {"id": x, "username": "xxx"}

    class Config:
        from_attributes = True