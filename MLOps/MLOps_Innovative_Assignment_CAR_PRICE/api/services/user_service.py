"""
User Service — CRUD operations for user management.
"""

from datetime import datetime, timezone
from bson import ObjectId

from api.database.connection import get_db
from api.auth.password import hash_password, verify_password
from api.auth.jwt_handler import create_access_token
from api.models.user import UserSignup, UserLogin


def create_user(user_data: UserSignup) -> dict:
    """
    Register a new user.
    
    Raises:
        ValueError: If username or email already exists.
    """
    db = get_db()

    # Check if user already exists
    if db.users.find_one({"username": user_data.username}):
        raise ValueError("Username already registered")
    if db.users.find_one({"email": user_data.email}):
        raise ValueError("Email already registered")

    # Create user document
    user_doc = {
        "username": user_data.username,
        "email": user_data.email,
        "hashed_password": hash_password(user_data.password),
        "role": user_data.role.value,
        "created_at": datetime.now(timezone.utc),
        "is_active": True
    }

    result = db.users.insert_one(user_doc)
    return {"message": "User created successfully", "user_id": str(result.inserted_id)}


def authenticate_user(login_data: UserLogin) -> dict:
    """
    Authenticate a user and return JWT token.
    
    Raises:
        ValueError: If credentials are invalid.
    """
    db = get_db()
    user = db.users.find_one({"username": login_data.username})

    if not user:
        raise ValueError("Invalid username or password")
    if not verify_password(login_data.password, user["hashed_password"]):
        raise ValueError("Invalid username or password")

    # Create JWT token
    token = create_access_token({
        "sub": str(user["_id"]),
        "role": user["role"],
        "username": user["username"]
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user["role"],
        "username": user["username"]
    }


def get_all_users() -> list:
    """Get all users (admin use)."""
    db = get_db()
    users = []
    for doc in db.users.find({}, {"hashed_password": 0}):
        doc["_id"] = str(doc["_id"])
        users.append(doc)
    return users
