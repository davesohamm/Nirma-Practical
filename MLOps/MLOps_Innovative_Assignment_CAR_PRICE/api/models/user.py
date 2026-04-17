"""
User Pydantic Schemas — Signup, Login, Response, Token
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    user = "user"
    admin = "admin"


class UserSignup(BaseModel):
    """Schema for user registration."""
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="Plain text password (will be hashed)")
    role: UserRole = Field(default=UserRole.user, description="User role: user or admin")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "securepass123",
                "role": "user"
            }
        }


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepass123"
            }
        }


class UserResponse(BaseModel):
    """Schema for user profile response."""
    id: str = Field(..., description="User ID")
    username: str
    email: str
    role: str
    is_active: bool = True


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str
