from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import datetime
import json

from ..database import get_db
from ..models.user import User
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse
from ..middleware.auth import get_current_active_user

router = APIRouter()


@router.get("", response_model=list[ProjectListResponse])
async def get_projects(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's projects."""
    skip = (page - 1) * page_size
    projects = db.query(Project).filter(
        Project.user_id == current_user.id
    ).order_by(Project.created_at.desc()).offset(skip).limit(page_size).all()
    
    return projects


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new project."""
    new_project = Project(
        user_id=current_user.id,
        name=project_data.name,
        description=project_data.description,
        content=project_data.content,
        url=project_data.url,
        cover_image=project_data.cover_image,
        tags=project_data.tags if project_data.tags else [],
        tech_stack=project_data.tech_stack if project_data.tech_stack else []
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return new_project


@router.get("/{project_id}")
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Return project with author info
    return {
        "id": project.id,
        "user_id": project.user_id,
        "name": project.name,
        "description": project.description,
        "content": project.content,
        "url": project.url,
        "cover_image": project.cover_image,
        "tags": project.tags,
        "tech_stack": project.tech_stack,
        "is_public": project.is_public,
        "published_at": project.published_at,
        "view_count": project.view_count,
        "like_count": project.like_count or 0,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "author": {
            "id": current_user.id,
            "username": current_user.username,
            "avatar": current_user.avatar
        }
    }


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a project."""
    # #region agent log
    log_data = {
        "location": "projects.py:update_project",
        "message": "Received update request",
        "data": {"project_id": project_id, "received_fields": project_data.model_dump()},
        "timestamp": int(datetime.now().timestamp() * 1000),
        "sessionId": "debug-session",
        "hypothesisId": "A",
        "runId": "pre-fix"
    }
    try:
        import os
        log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".bitfun", "debug.log")
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(log_data) + "\n")
    except Exception as e:
        print(f"Debug log error: {e}")
    # #endregion
    
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project_data.name:
        project.name = project_data.name
    
    if project_data.description:
        project.description = project_data.description
    
    # content 字段允许设置为空或更新
    if project_data.content is not None:
        project.content = project_data.content
    
    if project_data.url:
        project.url = project_data.url
    
    if project_data.cover_image:
        project.cover_image = project_data.cover_image
    
    if project_data.tags:
        project.tags = project_data.tags
    
    if project_data.tech_stack:
        project.tech_stack = project_data.tech_stack
    
    # #region agent log
    log_data2 = {
        "location": "projects.py:update_project",
        "message": "Project model fields",
        "data": {"model_has_content": hasattr(project, 'content'), "model_fields": [c.name for c in Project.__table__.columns]},
        "timestamp": int(datetime.now().timestamp() * 1000),
        "sessionId": "debug-session",
        "hypothesisId": "B",
        "runId": "pre-fix"
    }
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_data2) + "\n")
    except Exception as e:
        print(f"Debug log error: {e}")
    # #endregion
    
    if project_data.is_public is not None:
        project.is_public = project_data.is_public
        # 设置发布时间（首次发布时）
        if project_data.is_public and not project.published_at:
            project.published_at = datetime.utcnow()
    
    db.commit()
    db.refresh(project)
    
    # #region agent log
    log_data3 = {
        "location": "projects.py:update_project",
        "message": "Update completed successfully",
        "data": {"project_id": project.id, "content_saved": project.content, "is_public": project.is_public},
        "timestamp": int(datetime.now().timestamp() * 1000),
        "sessionId": "debug-session",
        "hypothesisId": "C",
        "runId": "pre-fix"
    }
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_data3) + "\n")
    except Exception as e:
        print(f"Debug log error: {e}")
    # #endregion
    
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a project."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()


@router.post("/{project_id}/publish", response_model=ProjectResponse)
async def publish_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Publish project to public domain."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.is_public = True
    project.published_at = datetime.utcnow()
    db.commit()
    db.refresh(project)
    
    return project


@router.post("/{project_id}/unpublish", response_model=ProjectResponse)
async def unpublish_project(
    project_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Unpublish project from public domain."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    project.is_public = False
    db.commit()
    db.refresh(project)
    
    return project