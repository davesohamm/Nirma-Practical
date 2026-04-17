"""
JWT Token Creation & Verification
Uses python-jose with HS256 algorithm.
"""

from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from api.config import settings


def create_access_token(data: dict) -> str:
    """
    Create a signed JWT access token.
    
    Args:
        data: Payload dict. Must contain 'sub' (user_id) and 'role'.
    
    Returns:
        Encoded JWT string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRY_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.
    
    Args:
        token: The encoded JWT string.
    
    Returns:
        Decoded payload dict.
    
    Raises:
        JWTError: If token is invalid or expired.
    """
    return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
