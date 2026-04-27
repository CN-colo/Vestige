from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LikeRequest(BaseModel):
    """点赞请求"""
    target_type: str  # 'article' or 'project'
    target_id: int


class LikeResponse(BaseModel):
    """点赞响应"""
    id: int
    user_id: int
    target_type: str
    target_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LikeStatus(BaseModel):
    """点赞状态"""
    is_liked: bool
    like_count: int