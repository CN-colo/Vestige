from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class TagSubscription(Base):
    """用户标签订阅模型"""
    __tablename__ = "tag_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tag = Column(String(50), nullable=False)  # 标签名称
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="tag_subscriptions")

    # Unique constraint: one user can only subscribe to a tag once
    __table_args__ = (
        UniqueConstraint('user_id', 'tag', name='unique_tag_subscription'),
    )