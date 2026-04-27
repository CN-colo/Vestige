from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.follow import Follow
from ..schemas.follow import FollowRequest, FollowResponse, FollowStats, UserWithFollowStatus
from ..middleware.auth import get_current_active_user, get_optional_user

router = APIRouter()


@router.post("", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
async def follow_user(
    request: FollowRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """关注一个用户"""
    # 不能关注自己
    if request.user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot follow yourself"
        )
    
    # 检查目标用户是否存在
    target_user = db.query(User).filter(User.id == request.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 检查是否已经关注
    existing_follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == request.user_id
    ).first()
    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user"
        )
    
    # 创建关注关系
    new_follow = Follow(
        follower_id=current_user.id,
        following_id=request.user_id
    )
    db.add(new_follow)
    db.commit()
    db.refresh(new_follow)
    
    return new_follow


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消关注一个用户"""
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()
    
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow relationship not found"
        )
    
    db.delete(follow)
    db.commit()


@router.get("/following", response_model=List[UserWithFollowStatus])
async def get_following(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取我关注的人列表"""
    follows = db.query(Follow).filter(Follow.follower_id == current_user.id).all()
    
    result = []
    for follow in follows:
        user = follow.following
        # 计算该用户的关注数和粉丝数
        following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
        followers_count = db.query(Follow).filter(Follow.following_id == user.id).count()
        
        result.append(UserWithFollowStatus(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            bio=user.bio,
            is_following=True,
            followers_count=followers_count,
            following_count=following_count
        ))
    
    return result


@router.get("/followers", response_model=List[UserWithFollowStatus])
async def get_followers(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取我的粉丝列表"""
    follows = db.query(Follow).filter(Follow.following_id == current_user.id).all()
    
    result = []
    for follow in follows:
        user = follow.follower
        # 计算该用户的关注数和粉丝数
        following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
        followers_count = db.query(Follow).filter(Follow.following_id == user.id).count()
        
        # 检查当前用户是否关注了该粉丝
        is_following = db.query(Follow).filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == user.id
        ).first() is not None
        
        result.append(UserWithFollowStatus(
            id=user.id,
            username=user.username,
            avatar=user.avatar,
            bio=user.bio,
            is_following=is_following,
            followers_count=followers_count,
            following_count=following_count
        ))
    
    return result


@router.get("/stats", response_model=FollowStats)
async def get_follow_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取当前用户的关注统计"""
    following_count = db.query(Follow).filter(Follow.follower_id == current_user.id).count()
    followers_count = db.query(Follow).filter(Follow.following_id == current_user.id).count()
    
    return FollowStats(
        following_count=following_count,
        followers_count=followers_count
    )


@router.get("/user/{user_id}", response_model=UserWithFollowStatus)
async def get_user_follow_info(
    user_id: int,
    current_user: User = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """获取指定用户的关注信息（包含当前用户是否关注了该用户）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 计算关注数和粉丝数
    following_count = db.query(Follow).filter(Follow.follower_id == user.id).count()
    followers_count = db.query(Follow).filter(Follow.following_id == user.id).count()
    
    # 检查当前用户是否关注了该用户
    is_following = False
    if current_user:
        is_following = db.query(Follow).filter(
            Follow.follower_id == current_user.id,
            Follow.following_id == user.id
        ).first() is not None
    
    return UserWithFollowStatus(
        id=user.id,
        username=user.username,
        avatar=user.avatar,
        bio=user.bio,
        is_following=is_following,
        followers_count=followers_count,
        following_count=following_count
    )


@router.get("/check/{user_id}")
async def check_following(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """检查当前用户是否关注了指定用户"""
    is_following = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first() is not None
    
    return {"is_following": is_following}