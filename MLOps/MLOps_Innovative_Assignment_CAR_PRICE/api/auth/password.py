"""
Password Hashing & Verification
Uses bcrypt directly (passlib has compatibility issues with bcrypt>=4.1).
"""

import bcrypt


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt."""
    password_bytes = plain_password.encode("utf-8")[:72]  # bcrypt 72-byte limit
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a bcrypt hash."""
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)
