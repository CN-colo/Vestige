from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.api_key import ApiKey
from ..schemas.api_key import ApiKeyCreate, ApiKeyUpdate, ApiKeyResponse, ApiKeyCreatedResponse
from ..middleware.auth import get_current_active_user
from ..utils.security import generate_api_key, hash_api_key

router = APIRouter()


@router.get("", response_model=list[ApiKeyResponse])
async def get_api_keys(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's API keys."""
    keys = db.query(ApiKey).filter(ApiKey.user_id == current_user.id).all()
    return keys


@router.post("", response_model=ApiKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: ApiKeyCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new API key."""
    # Generate raw key
    raw_key = generate_api_key()
    hashed_key = hash_api_key(raw_key)
    
    new_key = ApiKey(
        user_id=current_user.id,
        key=hashed_key,
        name=key_data.name,
        permissions=key_data.permissions or ["read:public"],
        expires_at=key_data.expires_at
    )
    db.add(new_key)
    db.commit()
    db.refresh(new_key)
    
    # Return with raw key (only shown once)
    return {
        "id": new_key.id,
        "key": raw_key,  # Raw key only shown on creation
        "name": new_key.name,
        "permissions": new_key.permissions,
        "expires_at": new_key.expires_at,
        "created_at": new_key.created_at
    }


@router.put("/{key_id}", response_model=ApiKeyResponse)
async def update_api_key(
    key_id: int,
    key_data: ApiKeyUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an API key."""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    if key_data.name:
        api_key.name = key_data.name
    
    if key_data.permissions:
        api_key.permissions = key_data.permissions
    
    if key_data.is_active is not None:
        api_key.is_active = key_data.is_active
    
    db.commit()
    db.refresh(api_key)
    
    return api_key


@router.delete("/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an API key."""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    db.delete(api_key)
    db.commit()