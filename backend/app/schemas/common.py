from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int


class MediaResponse(BaseModel):
    id: int
    filename: str
    original_name: str
    file_path: str
    file_size: int
    mime_type: str
    created_at: datetime

    class Config:
        from_attributes = True


class SearchResult(BaseModel):
    type: str  # "article" or "project"
    id: int
    title: Optional[str] = None  # article title or project name
    summary: Optional[str] = None
    content: Optional[str] = None
    author: Optional[dict] = None
    created_at: Optional[datetime] = None