from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from ..database import get_db
from ..models.user import User
from ..models.api_key import ApiKey
from ..models.article import Article
from ..models.project import Project
from ..schemas.article import ArticleCreate, ArticleUpdate
from ..schemas.project import ProjectCreate, ProjectUpdate
from ..schemas.common import SearchResult
from ..utils.security import verify_api_key, hash_api_key


router = APIRouter()


async def verify_api_key_auth(
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> ApiKey:
    """Verify API Key authentication and return the key object."""
    # Find key by hash
    hashed_key = hash_api_key(x_api_key)
    api_key = db.query(ApiKey).filter(ApiKey.key == hashed_key).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    if not api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is deactivated"
        )
    
    # Check expiration
    if api_key.expires_at and api_key.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key has expired"
        )
    
    # Update last used
    api_key.last_used_at = datetime.utcnow()
    db.commit()
    
    return api_key


def check_permission(api_key: ApiKey, permission: str) -> bool:
    """Check if API key has specific permission."""
    permissions = api_key.permissions or []
    return permission in permissions


@router.get("/search")
async def search_public(
    query: str = Query(None),
    type: str = Query(None),  # "article" or "project"
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Search public domain content."""
    if not check_permission(api_key, "read:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have read permission"
        )
    
    skip = (page - 1) * page_size
    results = []
    
    if not type or type == "article":
        articles = db.query(Article).filter(
            Article.is_public == True,
            Article.title.contains(query) if query else True
        ).offset(skip).limit(page_size).all()
        
        for article in articles:
            author = db.query(User).filter(User.id == article.user_id).first()
            results.append({
                "type": "article",
                "id": article.id,
                "title": article.title,
                "summary": article.summary,
                "author": {"id": author.id, "username": author.username} if author else None,
                "published_at": article.published_at,
                "view_count": article.view_count
            })
    
    if not type or type == "project":
        projects = db.query(Project).filter(
            Project.is_public == True,
            Project.name.contains(query) if query else True
        ).offset(skip).limit(page_size).all()
        
        for project in projects:
            author = db.query(User).filter(User.id == project.user_id).first()
            results.append({
                "type": "project",
                "id": project.id,
                "title": project.name,
                "summary": project.description[:200] if project.description else None,
                "author": {"id": author.id, "username": author.username} if author else None,
                "published_at": project.published_at,
                "view_count": project.view_count
            })
    
    return {
        "items": results,
        "total": len(results),
        "page": page,
        "page_size": page_size
    }


@router.post("/articles", status_code=status.HTTP_201_CREATED)
async def create_article_ai(
    article_data: ArticleCreate,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Create a public article via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    new_article = Article(
        user_id=api_key.user_id,
        title=article_data.title,
        content=article_data.content,
        content_type=article_data.content_type or "markdown",
        cover_image=article_data.cover_image,
        summary=article_data.summary,
        tags=article_data.tags or [],
        is_public=True,
        published_at=datetime.utcnow()
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    
    # Build preview URL
    preview_url = f"/article/{new_article.id}"
    
    return {
        "id": new_article.id,
        "title": new_article.title,
        "content_type": new_article.content_type,
        "preview_url": preview_url,
        "is_public": True,
        "created_at": new_article.created_at
    }


@router.get("/articles/{article_id}")
async def get_article_ai(
    article_id: int,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Get a public article via AI API."""
    if not check_permission(api_key, "read:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have read permission"
        )
    
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.is_public == True
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found or not public"
        )
    
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "content_type": article.content_type,
        "cover_image": article.cover_image,
        "summary": article.summary,
        "tags": article.tags,
        "view_count": article.view_count,
        "created_at": article.created_at,
        "published_at": article.published_at
    }


@router.put("/articles/{article_id}")
async def update_article_ai(
    article_id: int,
    article_data: ArticleUpdate,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Update a public article via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == api_key.user_id,
        Article.is_public == True
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found or not owned by API key owner"
        )
    
    if article_data.title:
        article.title = article_data.title
    if article_data.content:
        article.content = article_data.content
    if article_data.content_type:
        article.content_type = article_data.content_type
    if article_data.cover_image:
        article.cover_image = article_data.cover_image
    if article_data.summary:
        article.summary = article_data.summary
    if article_data.tags:
        article.tags = article_data.tags
    
    db.commit()
    db.refresh(article)
    
    return {
        "id": article.id,
        "title": article.title,
        "content_type": article.content_type,
        "updated_at": article.updated_at
    }


@router.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article_ai(
    article_id: int,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Delete a public article via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    article = db.query(Article).filter(
        Article.id == article_id,
        Article.user_id == api_key.user_id,
        Article.is_public == True
    ).first()
    
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found or not owned by API key owner"
        )
    
    db.delete(article)
    db.commit()


@router.post("/projects", status_code=status.HTTP_201_CREATED)
async def create_project_ai(
    project_data: ProjectCreate,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Create a public project via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    new_project = Project(
        user_id=api_key.user_id,
        name=project_data.name,
        description=project_data.description,
        url=project_data.url,
        cover_image=project_data.cover_image,
        tags=project_data.tags or [],
        tech_stack=project_data.tech_stack or [],
        is_public=True,
        published_at=datetime.utcnow()
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {
        "id": new_project.id,
        "name": new_project.name,
        "is_public": True,
        "created_at": new_project.created_at
    }


@router.get("/projects/{project_id}")
async def get_project_ai(
    project_id: int,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Get a public project via AI API."""
    if not check_permission(api_key, "read:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have read permission"
        )
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.is_public == True
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not public"
        )
    
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "url": project.url,
        "cover_image": project.cover_image,
        "tags": project.tags,
        "tech_stack": project.tech_stack,
        "view_count": project.view_count,
        "created_at": project.created_at,
        "published_at": project.published_at
    }


@router.put("/projects/{project_id}")
async def update_project_ai(
    project_id: int,
    project_data: ProjectUpdate,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Update a public project via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == api_key.user_id,
        Project.is_public == True
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not owned by API key owner"
        )
    
    if project_data.name:
        project.name = project_data.name
    if project_data.description:
        project.description = project_data.description
    if project_data.url:
        project.url = project_data.url
    if project_data.cover_image:
        project.cover_image = project_data.cover_image
    if project_data.tags:
        project.tags = project_data.tags
    if project_data.tech_stack:
        project.tech_stack = project_data.tech_stack
    
    db.commit()
    db.refresh(project)
    
    return {
        "id": project.id,
        "name": project.name,
        "updated_at": project.updated_at
    }


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_ai(
    project_id: int,
    api_key: ApiKey = Depends(verify_api_key_auth),
    db: Session = Depends(get_db)
):
    """Delete a public project via AI API."""
    if not check_permission(api_key, "write:public"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key does not have write permission"
        )
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == api_key.user_id,
        Project.is_public == True
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or not owned by API key owner"
        )
    
    db.delete(project)
    db.commit()