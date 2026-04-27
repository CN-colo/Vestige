from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import json

from ..database import get_db
from ..models.user import User
from ..models.article import Article
from ..schemas.article import ArticleCreate, ArticleUpdate, ArticleResponse, ArticleListResponse
from ..middleware.auth import get_current_active_user

router = APIRouter()


@router.get("", response_model=list[ArticleListResponse])
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's articles."""
    skip = (page - 1) * page_size
    articles = db.query(Article).filter(
        Article.user_id == current_user.id
    ).order_by(Article.created_at.desc()).offset(skip).limit(page_size).all()
    
    return articles


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_data: ArticleCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new article."""
    new_article = Article(
        user_id=current_user.id,
        title=article_data.title,
        content=article_data.content,
        cover_image=article_data.cover_image,
        summary=article_data.summary,
        tags=article_data.tags if article_data.tags else []
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    return new_article


@router.get("/{article_id}")
async def get_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific article."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    # Return article with author info
    return {
        "id": article.id,
        "user_id": article.user_id,
        "title": article.title,
        "content": article.content,
        "cover_image": article.cover_image,
        "summary": article.summary,
        "tags": article.tags,
        "is_public": article.is_public,
        "published_at": article.published_at,
        "view_count": article.view_count,
        "like_count": article.like_count or 0,
        "created_at": article.created_at,
        "updated_at": article.updated_at,
        "author": {
            "id": current_user.id,
            "username": current_user.username,
            "avatar": current_user.avatar
        }
    }


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an article."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    if article_data.title:
        article.title = article_data.title
    
    if article_data.content:
        article.content = article_data.content
    
    if article_data.cover_image:
        article.cover_image = article_data.cover_image
    
    if article_data.summary:
        article.summary = article_data.summary
    
    if article_data.tags:
        article.tags = article_data.tags
    
    db.commit()
    db.refresh(article)
    
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an article."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    db.delete(article)
    db.commit()


@router.post("/{article_id}/publish", response_model=ArticleResponse)
async def publish_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Publish article to public domain."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article.is_public = True
    article.published_at = datetime.utcnow()
    db.commit()
    db.refresh(article)
    
    return article


@router.post("/{article_id}/unpublish", response_model=ArticleResponse)
async def unpublish_article(
    article_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Unpublish article from public domain."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == current_user.id
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article.is_public = False
    db.commit()
    db.refresh(article)
    
    return article