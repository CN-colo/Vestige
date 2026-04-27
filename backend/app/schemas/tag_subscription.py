from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TagSubscriptionCreate(BaseModel):
    """创建标签订阅"""
    tag: str = Field(..., min_length=1, max_length=50)


class TagSubscriptionResponse(BaseModel):
    """标签订阅响应"""
    id: int
    tag: str
    created_at: datetime

    class Config:
        from_attributes = True


class TagSubscriptionList(BaseModel):
    """用户订阅的标签列表"""
    tags: List[str]
    total: int