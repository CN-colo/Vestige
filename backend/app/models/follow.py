from sqlalchemy import Column, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Follow(Base):
    """用户关注关系模型"""
    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 关注者
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 被关注者
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")

    # Unique constraint: one user can only follow another user once
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
    )