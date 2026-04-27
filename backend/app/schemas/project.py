from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Any
from datetime import datetime


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str
    url: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    url: Optional[str] = Field(None, max_length=500)
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    url: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
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


class ProjectListResponse(BaseModel):
    id: int
    name: str
    description: str
    url: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    is_public: bool
    published_at: Optional[datetime] = None
    view_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectPublicResponse(BaseModel):
    id: int
    name: str
    description: str
    url: Optional[str] = None
    cover_image: Optional[str] = None
    tags: Optional[List[str]] = None
    tech_stack: Optional[List[str]] = None
    published_at: Optional[datetime] = None
    view_count: int
    author: Optional[dict] = None

    class Config:
        from_attributes = True