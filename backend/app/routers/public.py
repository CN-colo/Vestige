from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import Optional, List, Literal

from ..database import get_db
from ..models.user import User
from ..models.article import Article
from ..models.project import Project
from ..schemas.article import ArticlePublicResponse
from ..schemas.project import ProjectPublicResponse
from ..schemas.user import UserPublic
from ..config import settings

router = APIRouter()


@router.get("/articles", response_model=dict)
async def get_public_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    tag: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get public articles list."""
    skip = (page - 1) * page_size
    
    query = db.query(Article).filter(Article.is_public == True)
    
    if search:
        query = query.filter(
            (Article.title.contains(search)) |
            (Article.content.contains(search)) |
            (Article.summary.contains(search))
        )
    
    if tag:
        # Search for tag in JSON array using LIKE
        query = query.filter(Article.tags.contains(f'"{tag}"'))
    
    # Get total count
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    articles = query.order_by(Article.published_at.desc()).offset(skip).limit(page_size).all()
    
    items = []
    for article in articles:
        author = db.query(User).filter(User.id == article.user_id).first()
        items.append({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "content_type": article.content_type or "markdown",
            "cover_image": article.cover_image,
            "summary": article.summary,
            "tags": article.tags,
            "published_at": article.published_at,
            "created_at": article.created_at,
            "view_count": article.view_count,
            "author": {"id": author.id, "username": author.username} if author else None
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/articles/{article_id}", response_model=dict)
async def get_public_article(article_id: int, db: Session = Depends(get_db)):
    """Get a specific public article."""
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_public == True
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found or not public"
        )
    
    # Increment view count
    article.view_count += 1
    db.commit()
    
    author = db.query(User).filter(User.id == article.user_id).first()
    
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "content_type": article.content_type or "markdown",
        "cover_image": article.cover_image,
        "summary": article.summary,
        "tags": article.tags,
        "published_at": article.published_at,
        "view_count": article.view_count,
        "like_count": article.like_count or 0,
        "created_at": article.created_at,
        "author": {"id": author.id, "username": author.username, "avatar": author.avatar, "bio": author.bio} if author else None
    }


@router.get("/projects", response_model=dict)
async def get_public_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    tag: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get public projects list."""
    skip = (page - 1) * page_size
    
    query = db.query(Project).filter(Project.is_public == True)
    
    if search:
        query = query.filter(
            (Project.name.contains(search)) |
            (Project.description.contains(search))
        )
    
    if tag:
        # Search for tag in tags or tech_stack JSON array
        query = query.filter(
            or_(
                Project.tags.contains(f'"{tag}"'),
                Project.tech_stack.contains(f'"{tag}"')
            )
        )
    
    total = query.count()
    total_pages = (total + page_size - 1) // page_size
    
    projects = query.order_by(Project.published_at.desc()).offset(skip).limit(page_size).all()
    
    items = []
    for project in projects:
        author = db.query(User).filter(User.id == project.user_id).first()
        items.append({
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "url": project.url,
            "cover_image": project.cover_image,
            "tags": project.tags,
            "tech_stack": project.tech_stack,
            "published_at": project.published_at,
            "created_at": project.created_at,
            "view_count": project.view_count,
            "author": {"id": author.id, "username": author.username} if author else None
        })
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/projects/{project_id}", response_model=dict)
async def get_public_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific public project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_public == True
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not public"
        )
    
    project.view_count += 1
    db.commit()
    
    author = db.query(User).filter(User.id == project.user_id).first()
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "url": project.url,
        "cover_image": project.cover_image,
        "tags": project.tags,
        "tech_stack": project.tech_stack,
        "published_at": project.published_at,
        "view_count": project.view_count,
        "like_count": project.like_count or 0,
        "created_at": project.created_at,
        "author": {"id": author.id, "username": author.username, "avatar": author.avatar, "bio": author.bio} if author else None
    }


@router.get("/all", response_model=dict)
async def get_public_all(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: str = Query(None),
    tag: str = Query(None),
    content_type: Literal["all", "article", "project"] = Query("all"),
    db: Session = Depends(get_db)
):
    """Get all public content (articles and projects) with unified interface."""
    skip = (page - 1) * page_size
    
    items = []
    
    # Fetch articles if needed
    if content_type in ["all", "article"]:
        article_query = db.query(Article).filter(Article.is_public == True)
        
        if search:
            article_query = article_query.filter(
                (Article.title.contains(search)) |
                (Article.content.contains(search)) |
                (Article.summary.contains(search))
            )
        
        if tag:
            article_query = article_query.filter(Article.tags.contains(f'"{tag}"'))
        
        articles = article_query.all()
        for article in articles:
            author = db.query(User).filter(User.id == article.user_id).first()
            items.append({
                "id": article.id,
                "type": "article",
                "title": article.title,
                "content": article.content,
                "content_type": article.content_type or "markdown",
                "cover_image": article.cover_image,
                "summary": article.summary,
                "tags": article.tags,
                "tech_stack": None,
                "url": None,
                "published_at": article.published_at,
                "created_at": article.created_at,
                "view_count": article.view_count,
                "author": {"id": author.id, "username": author.username} if author else None
            })
    
    # Fetch projects if needed
    if content_type in ["all", "project"]:
        project_query = db.query(Project).filter(Project.is_public == True)
        
        if search:
            project_query = project_query.filter(
                (Project.name.contains(search)) |
                (Project.description.contains(search))
            )
        
        if tag:
            project_query = project_query.filter(
                or_(
                    Project.tags.contains(f'"{tag}"'),
                    Project.tech_stack.contains(f'"{tag}"')
                )
            )
        
        projects = project_query.all()
        for project in projects:
            author = db.query(User).filter(User.id == project.user_id).first()
            items.append({
                "id": project.id,
                "type": "project",
                "title": project.name,
                "content": project.description,
                "cover_image": project.cover_image,
                "summary": None,
                "tags": project.tags,
                "tech_stack": project.tech_stack,
                "url": project.url,
                "published_at": project.published_at,
                "created_at": project.created_at,
                "view_count": project.view_count,
                "author": {"id": author.id, "username": author.username} if author else None
            })
    
    # Sort by published_at descending
    items.sort(key=lambda x: x["published_at"] or x["created_at"], reverse=True)
    
    # Paginate
    total = len(items)
    total_pages = (total + page_size - 1) // page_size
    paginated_items = items[skip:skip + page_size]
    
    return {
        "items": paginated_items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }


@router.get("/tags", response_model=dict)
async def get_all_tags(db: Session = Depends(get_db)):
    """Get all unique tags from public articles and projects."""
    tags_set = set()
    
    # Get tags from articles
    articles = db.query(Article).filter(Article.is_public == True, Article.tags != None).all()
    for article in articles:
        if article.tags:
            for tag in article.tags:
                tags_set.add(tag)
    
    # Get tags and tech_stack from projects
    projects = db.query(Project).filter(Project.is_public == True).all()
    for project in projects:
        if project.tags:
            for tag in project.tags:
                tags_set.add(tag)
        if project.tech_stack:
            for tech in project.tech_stack:
                tags_set.add(tech)
    
    return {
        "tags": sorted(list(tags_set))
    }


@router.get("/users/{user_id}", response_model=dict)
async def get_public_user(user_id: int, db: Session = Depends(get_db)):
    """Get a user's public profile and their public content."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's public articles count
    articles_count = db.query(Article).filter(
        Article.user_id == user_id,
        Article.is_public == True
    ).count()
    
    # Get user's public projects count
    projects_count = db.query(Project).filter(
        Project.user_id == user_id,
        Project.is_public == True
    ).count()
    
    return {
        "id": user.id,
        "username": user.username,
        "avatar": user.avatar,
        "bio": user.bio,
        "contact": user.contact,
        "articles_count": articles_count,
        "projects_count": projects_count,
        "created_at": user.created_at
    }


@router.get("/card/{user_id}", response_model=dict)
async def get_user_card(user_id: int, db: Session = Depends(get_db)):
    """Get a user's business card with detailed information."""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if card is enabled
    if not user.card_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has disabled card sharing"
        )
    
    # Get user's public articles
    articles = db.query(Article).filter(
        Article.user_id == user_id,
        Article.is_public == True
    ).order_by(Article.published_at.desc()).limit(10).all()
    
    articles_list = [{
        "id": a.id,
        "title": a.title,
        "summary": a.summary,
        "cover_image": a.cover_image,
        "view_count": a.view_count,
        "published_at": a.published_at
    } for a in articles]
    
    # Get user's public projects
    projects = db.query(Project).filter(
        Project.user_id == user_id,
        Project.is_public == True
    ).order_by(Project.published_at.desc()).limit(10).all()
    
    projects_list = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "cover_image": p.cover_image,
        "url": p.url,
        "tech_stack": p.tech_stack,
        "view_count": p.view_count,
        "published_at": p.published_at
    } for p in projects]
    
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "bio": user.bio,
        "contact": user.contact,
        "articles_count": len(articles_list),
        "projects_count": len(projects_list),
        "articles": articles_list,
        "projects": projects_list,
        "created_at": user.created_at
    }


@router.get("/agent-guide")
async def get_agent_guide():
    """Get Agent guide URL for AI integration."""
    if settings.DEBUG:
        # 本地调试时，文档挂载在 /docs-static
        base = f"{settings.effective_base_url}/docs-static"
    else:
        # 生产环境，文档直接在根目录
        base = settings.BASE_URL
    return {
        "agent_guide_url": f"{base}/AGENT_GUIDE.md",
        "ai_api_url": f"{base}/AI_API.md"
    }