"""
FastAPI Dependency Injection for Authentication & Authorization.
Extracts current user from JWT, enforces role-based access.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from api.auth.jwt_handler import decode_access_token
from api.database.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Extract and validate the current user from the JWT token.
    Returns the user document from MongoDB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        if user_id is None or role is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Fetch user from DB
    from bson import ObjectId
    db = get_db()
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception

    # Convert ObjectId to string for serialization
    user["_id"] = str(user["_id"])
    return user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency: only allows admin users."""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency: allows any authenticated user (user or admin)."""
    return current_user
