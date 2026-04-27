from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Literal

from ..database import get_db
from ..models.user import User
from ..models.article import Article
from ..models.project import Project
from ..models.favorite import Favorite
from ..schemas.favorite import FavoriteCreate, FavoriteResponse, FavoriteWithItemResponse
from ..middleware.auth import get_current_active_user

router = APIRouter()


@router.post("", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    favorite_data: FavoriteCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add an article or project to favorites."""
    # Check if target exists and is public
    if favorite_data.target_type == "article":
        target = db.query(Article).filter(Article.id == favorite_data.target_id).first()
        if not target or not target.is_public:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Article not found or not public"
            )
    elif favorite_data.target_type == "project":
        target = db.query(Project).filter(Project.id == favorite_data.target_id).first()
        if not target or not target.is_public:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found or not public"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid target type"
        )
    
    # Check if already favorited
    existing = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.target_type == favorite_data.target_type,
        Favorite.target_id == favorite_data.target_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already favorited"
        )
    
    # Create favorite
    new_favorite = Favorite(
        user_id=current_user.id,
        target_type=favorite_data.target_type,
        target_id=favorite_data.target_id
    )
    db.add(new_favorite)
    db.commit()
    db.refresh(new_favorite)
    
    return new_favorite


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    target_type: Literal["article", "project"],
    target_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove an article or project from favorites."""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.target_type == target_type,
        Favorite.target_id == target_id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    db.delete(favorite)
    db.commit()


@router.get("", response_model=list[FavoriteWithItemResponse])
async def get_favorites(
    target_type: Literal["article", "project"] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's favorites list."""
    skip = (page - 1) * page_size
    query = db.query(Favorite).filter(Favorite.user_id == current_user.id)
    
    if target_type:
        query = query.filter(Favorite.target_type == target_type)
    
    favorites = query.order_by(Favorite.created_at.desc()).offset(skip).limit(page_size).all()
    
    # Build response with item details
    result = []
    for favorite in favorites:
        item_data = None
        if favorite.target_type == "article":
            article = db.query(Article).filter(Article.id == favorite.target_id).first()
            if article:
                item_data = {
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "cover_image": article.cover_image,
                    "view_count": article.view_count,
                    "author": {
                        "id": article.author.id,
                        "username": article.author.username,
                        "avatar": article.author.avatar
                    }
                }
        elif favorite.target_type == "project":
            project = db.query(Project).filter(Project.id == favorite.target_id).first()
            if project:
                item_data = {
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "cover_image": project.cover_image,
                    "view_count": project.view_count,
                    "author": {
                        "id": project.author.id,
                        "username": project.author.username,
                        "avatar": project.author.avatar
                    }
                }
        
        result.append(FavoriteWithItemResponse(
            id=favorite.id,
            target_type=favorite.target_type,
            target_id=favorite.target_id,
            created_at=favorite.created_at,
            item=item_data
        ))
    
    return result


@router.get("/check")
async def check_favorite(
    target_type: Literal["article", "project"],
    target_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Check if an item is favorited by current user."""
    favorite = db.query(Favorite).filter(
        Favorite.user_id == current_user.id,
        Favorite.target_type == target_type,
        Favorite.target_id == target_id
    ).first()
    
    return {"is_favorited": favorite is not None}