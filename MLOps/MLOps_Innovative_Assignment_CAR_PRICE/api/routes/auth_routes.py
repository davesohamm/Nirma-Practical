"""
Authentication Routes — Signup, Login, Profile
POST /auth/signup, POST /auth/login, GET /auth/me
"""

from fastapi import APIRouter, HTTPException, status, Depends

from api.models.user import UserSignup, UserLogin, UserResponse, TokenResponse
from api.services.user_service import create_user, authenticate_user
from api.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user_data: UserSignup):
    """Register a new user."""
    try:
        result = create_user(user_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Signup failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin):
    """Authenticate user and return JWT token."""
    try:
        result = authenticate_user(login_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Login failed: {str(e)}")


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: dict = Depends(get_current_user)):
    """Get current user's profile."""
    return UserResponse(
        id=current_user["_id"],
        username=current_user["username"],
        email=current_user["email"],
        role=current_user["role"],
        is_active=current_user.get("is_active", True)
    )
