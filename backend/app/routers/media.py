from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
import os
import uuid
from datetime import datetime

from ..database import get_db
from ..models.user import User
from ..models.media import Media
from ..schemas.common import MediaResponse
from ..middleware.auth import get_current_active_user
from ..config import settings

router = APIRouter()


@router.post("/upload", response_model=MediaResponse)
async def upload_media(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload an image file."""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File type not allowed. Only images are accepted."
        )
    
    # Validate file size
    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds maximum allowed size ({settings.MAX_UPLOAD_SIZE} bytes)"
        )
    
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    
    # Create upload directory if not exists
    upload_dir = os.path.abspath(settings.UPLOAD_DIR)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_dir, unique_filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Save to database
    media = Media(
        user_id=current_user.id,
        filename=unique_filename,
        original_name=file.filename,
        file_path=file_path,
        file_size=file_size,
        mime_type=file.content_type
    )
    db.add(media)
    db.commit()
    db.refresh(media)
    
    return media


@router.get("/{media_id}")
async def get_media(
    media_id: int,
    db: Session = Depends(get_db)
):
    """Get media file info."""
    media = db.query(Media).filter(Media.id == media_id).first()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found"
        )
    
    return {
        "id": media.id,
        "filename": media.filename,
        "original_name": media.original_name,
        "file_path": media.file_path,
        "file_size": media.file_size,
        "mime_type": media.mime_type,
        "url": f"/uploads/{media.filename}",
        "created_at": media.created_at
    }


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a media file."""
    media = db.query(Media).filter(
        Media.id == media_id,
        Media.user_id == current_user.id
    ).first()
    
    if not media:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found or not owned by you"
        )
    
    # Delete file from disk
    if os.path.exists(media.file_path):
        os.remove(media.file_path)
    
    # Delete from database
    db.delete(media)
    db.commit()