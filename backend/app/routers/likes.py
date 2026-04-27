from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Literal

from ..database import get_db
from ..models.user import User
from ..models.like import Like
from ..models.article import Article
from ..models.project import Project
from ..schemas.like import LikeRequest, LikeResponse, LikeStatus
from ..middleware.auth import get_current_active_user, get_optional_user

router = APIRouter()

TargetType = Literal["article", "project"]


@router.post("", response_model=LikeResponse, status_code=status.HTTP_201_CREATED)
async def create_like(
    request: LikeRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """点赞"""
    # 验证目标类型
    if request.target_type not in ["article", "project"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid target type. Must be 'article' or 'project'"
        )
    
    # 验证目标是否存在且是公开的
    if request.target_type == "article":
        target = db.query(Article).filter(Article.id == request.target_id).first()
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
        if not target.is_public:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot like private content")
    else:
        target = db.query(Project).filter(Project.id == request.target_id).first()
        if not target:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
        if not target.is_public:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot like private content")
    
    # 检查是否已经点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.target_type == request.target_type,
        Like.target_id == request.target_id
    ).first()
    
    if existing_like:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already liked this content")
    
    # 创建点赞
    new_like = Like(
        user_id=current_user.id,
        target_type=request.target_type,
        target_id=request.target_id
    )
    db.add(new_like)
    
    # 更新点赞计数
    target.like_count = (target.like_count or 0) + 1
    
    db.commit()
    db.refresh(new_like)
    
    return new_like


@router.delete("/{target_type}/{target_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    target_type: str,
    target_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消点赞"""
    # 验证目标类型
    if target_type not in ["article", "project"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid target type"
        )
    
    like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.target_type == target_type,
        Like.target_id == target_id
    ).first()
    
    if not like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like not found")
    
    # 更新点赞计数
    if target_type == "article":
        target = db.query(Article).filter(Article.id == target_id).first()
    else:
        target = db.query(Project).filter(Project.id == target_id).first()
    
    if target and target.like_count > 0:
        target.like_count -= 1
    
    db.delete(like)
    db.commit()


@router.get("/status/{target_type}/{target_id}", response_model=LikeStatus)
async def get_like_status(
    target_type: str,
    target_id: int,
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取点赞状态（是否已点赞、点赞数）"""
    # 验证目标类型
    if target_type not in ["article", "project"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid target type"
        )
    
    # 获取目标内容的点赞数
    if target_type == "article":
        target = db.query(Article).filter(Article.id == target_id).first()
    else:
        target = db.query(Project).filter(Project.id == target_id).first()
    
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Content not found")
    
    like_count = target.like_count or 0
    
    # 检查当前用户是否已点赞
    is_liked = False
    if current_user:
        is_liked = db.query(Like).filter(
            Like.user_id == current_user.id,
            Like.target_type == target_type,
            Like.target_id == target_id
        ).first() is not None
    
    return LikeStatus(is_liked=is_liked, like_count=like_count)


@router.get("/my", response_model=List[LikeResponse])
async def get_my_likes(
    target_type: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取我的点赞列表"""
    query = db.query(Like).filter(Like.user_id == current_user.id)
    
    if target_type:
        if target_type not in ["article", "project"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target type")
        query = query.filter(Like.target_type == target_type)
    
    likes = query.all()
    return likes


@router.get("/users/{target_type}/{target_id}")
async def get_like_users(
    target_type: str,
    target_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取点赞该内容的用户列表"""
    if target_type not in ["article", "project"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid target type")
    
    likes = db.query(Like).filter(
        Like.target_type == target_type,
        Like.target_id == target_id
    ).limit(limit).all()
    
    users = []
    for like in likes:
        users.append({
            "id": like.user.id,
            "username": like.user.username,
            "avatar": like.user.avatar
        })
    
    return {"users": users, "total": len(users)}