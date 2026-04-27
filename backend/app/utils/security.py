from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib

from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config import settings


# Use argon2 instead of bcrypt for better Python 3.13 compatibility
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT access token."""
    try:
        print(f"DEBUG decode: SECRET_KEY={settings.SECRET_KEY[:20]}..., ALGORITHM={settings.ALGORITHM}")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(f"DEBUG decode: Success, payload={payload}")
        return payload
    except JWTError as e:
        print(f"DEBUG decode: JWTError - {e}")
        return None


def generate_api_key() -> str:
    """Generate a random API key (32 bytes, hex encoded)."""
    return secrets.token_hex(32)


def hash_api_key(key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256(key.encode()).hexdigest()


def verify_api_key(key: str, hashed_key: str) -> bool:
    """Verify an API key against a hash."""
    return hash_api_key(key) == hashed_key