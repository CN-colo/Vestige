from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.tag_subscription import TagSubscription
from ..models.article import Article
from ..models.project import Project
from ..schemas.tag_subscription import TagSubscriptionCreate, TagSubscriptionResponse, TagSubscriptionList
from ..middleware.auth import get_current_active_user

router = APIRouter()


@router.post("", response_model=TagSubscriptionResponse, status_code=status.HTTP_201_CREATED)
async def subscribe_tag(
    request: TagSubscriptionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """订阅一个标签"""
    tag = request.tag.strip().lower()
    
    # 检查是否已经订阅
    existing = db.query(TagSubscription).filter(
        TagSubscription.user_id == current_user.id,
        TagSubscription.tag == tag
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already subscribed to this tag"
        )
    
    # 创建订阅
    new_subscription = TagSubscription(
        user_id=current_user.id,
        tag=tag
    )
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    
    return new_subscription


@router.delete("/{tag}", status_code=status.HTTP_204_NO_CONTENT)
async def unsubscribe_tag(
    tag: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """取消订阅一个标签"""
    tag = tag.strip().lower()
    
    subscription = db.query(TagSubscription).filter(
        TagSubscription.user_id == current_user.id,
        TagSubscription.tag == tag
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tag subscription not found"
        )
    
    db.delete(subscription)
    db.commit()


@router.get("", response_model=TagSubscriptionList)
async def get_subscriptions(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取用户订阅的所有标签"""
    subscriptions = db.query(TagSubscription).filter(
        TagSubscription.user_id == current_user.id
    ).all()
    
    tags = [sub.tag for sub in subscriptions]
    
    return TagSubscriptionList(
        tags=tags,
        total=len(tags)
    )


@router.get("/feed")
async def get_subscription_feed(
    page: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取订阅标签相关的内容推送"""
    # 获取用户订阅的标签
    subscriptions = db.query(TagSubscription).filter(
        TagSubscription.user_id == current_user.id
    ).all()
    
    subscribed_tags = [sub.tag for sub in subscriptions]
    
    if not subscribed_tags:
        return {
            "articles": [],
            "projects": [],
            "total_articles": 0,
            "total_projects": 0,
            "page": page,
            "page_size": page_size
        }
    
    # 查询包含订阅标签的公开文章
    articles_query = db.query(Article).filter(
        Article.is_public == True,
        Article.tags != None
    )
    
    # 由于tags是JSON字段，需要用JSON查询
    # SQLite的JSON查询方式：检查tags是否包含任一订阅的标签
    articles = []
    for article in articles_query.all():
        if article.tags:
            article_tags = [t.lower() for t in article.tags]
            if any(tag in article_tags for tag in subscribed_tags):
                articles.append({
                    "id": article.id,
                    "title": article.title,
                    "summary": article.summary,
                    "cover_image": article.cover_image,
                    "tags": article.tags,
                    "view_count": article.view_count,
                    "like_count": article.like_count,
                    "published_at": article.published_at,
                    "author": {
                        "id": article.author.id,
                        "username": article.author.username,
                        "avatar": article.author.avatar
                    }
                })
    
    # 查询包含订阅标签的公开作品
    projects_query = db.query(Project).filter(
        Project.is_public == True,
        Project.tags != None
    )
    
    projects = []
    for project in projects_query.all():
        if project.tags:
            project_tags = [t.lower() for t in project.tags]
            if any(tag in project_tags for tag in subscribed_tags):
                projects.append({
                    "id": project.id,
                    "name": project.name,
                    "description": project.description,
                    "cover_image": project.cover_image,
                    "tags": project.tags,
                    "tech_stack": project.tech_stack,
                    "view_count": project.view_count,
                    "like_count": project.like_count,
                    "published_at": project.published_at,
                    "author": {
                        "id": project.author.id,
                        "username": project.author.username,
                        "avatar": project.author.avatar
                    }
                })
    
    # 分页
    start = (page - 1) * page_size
    end = start + page_size
    
    return {
        "articles": articles[start:end],
        "projects": projects[start:end],
        "total_articles": len(articles),
        "total_projects": len(projects),
        "page": page,
        "page_size": page_size,
        "subscribed_tags": subscribed_tags
    }


@router.get("/popular")
async def get_popular_tags(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """获取热门标签（根据订阅数量）"""
    # 统计每个标签的订阅数
    result = db.query(
        TagSubscription.tag,
        func.count(TagSubscription.id).label('count')
    ).group_by(TagSubscription.tag).order_by(func.count(TagSubscription.id).desc()).limit(limit).all()
    
    return [{"tag": row.tag, "count": row.count} for row in result]