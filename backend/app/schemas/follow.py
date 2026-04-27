from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class FollowRequest(BaseModel):
    """关注请求"""
    user_id: int  # 要关注的用户ID


class FollowResponse(BaseModel):
    """关注响应"""
    id: int
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FollowStats(BaseModel):
    """用户关注统计"""
    following_count: int  # 关注了多少人
    followers_count: int  # 有多少粉丝


class UserWithFollowStatus(BaseModel):
    """带关注状态的用户信息"""
    id: int
    username: str
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_following: bool = False  # 当前用户是否关注了此人
    followers_count: int = 0
    following_count: int = 0

    class Config:
        from_attributes = True