from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class FavoriteCreate(BaseModel):
    target_type: Literal["article", "project"] = Field(..., description="Type of the item to favorite")
    target_id: int = Field(..., description="ID of the item to favorite")


class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    target_type: str
    target_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FavoriteWithItemResponse(BaseModel):
    """Favorite response with the favorited item details"""
    id: int
    target_type: str
    target_id: int
    created_at: datetime
    item: Optional[dict] = None  # The actual article or project data

    class Config:
        from_attributes = True