from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import User
from ..models.comment import Comment
from ..schemas.comment import CommentCreate, CommentUpdate, CommentResponse, CommentAuthorResponse
from ..middleware.auth import get_current_active_user

router = APIRouter()


def build_comment_response(comment: Comment, db: Session) -> dict:
    """Build a comment response with author info and nested replies."""
    author = db.query(User).filter(User.id == comment.user_id).first()
    
    # Get replies for this comment
    replies = db.query(Comment).filter(
        Comment.parent_id == comment.id
    ).order_by(Comment.created_at.asc()).all()
    
    return {
        "id": comment.id,
        "user_id": comment.user_id,
        "content_type": comment.content_type,
        "content_id": comment.content_id,
        "content": comment.content,
        "parent_id": comment.parent_id,
        "created_at": comment.created_at,
        "updated_at": comment.updated_at,
        "author": {
            "id": author.id,
            "username": author.username,
            "avatar": author.avatar
        } if author else None,
        "replies": [build_comment_response(reply, db) for reply in replies]
    }


@router.get("", response_model=List[dict])
async def get_comments(
    content_type: str = Query(..., pattern="^(article|project)$"),
    content_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Get comments for an article or project (public access)."""
    # Only get top-level comments (parent_id is None)
    comments = db.query(Comment).filter(
        Comment.content_type == content_type,
        Comment.content_id == content_id,
        Comment.parent_id == None
    ).order_by(Comment.created_at.desc()).all()
    
    return [build_comment_response(comment, db) for comment in comments]


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new comment (requires authentication)."""
    new_comment = Comment(
        user_id=current_user.id,
        content_type=comment_data.content_type,
        content_id=comment_data.content_id,
        content=comment_data.content,
        parent_id=comment_data.parent_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    
    return build_comment_response(new_comment, db)


@router.put("/{comment_id}", response_model=dict)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a comment (only the author can update)."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own comments"
        )
    
    comment.content = comment_data.content
    db.commit()
    db.refresh(comment)
    
    return build_comment_response(comment, db)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a comment (only the author can delete)."""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
    
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments"
        )
    
    db.delete(comment)
    db.commit()