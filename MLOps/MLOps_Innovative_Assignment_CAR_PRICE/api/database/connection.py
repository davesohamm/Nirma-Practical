"""
MongoDB Connection Manager
Uses pymongo (synchronous) with MongoClient.
"""

from pymongo import MongoClient
from pymongo.database import Database
from api.config import settings

client: MongoClient = None
db: Database = None


def connect_db():
    """Connect to MongoDB and create indexes."""
    global client, db
    client = MongoClient(settings.MONGO_URL)
    db = client[settings.MONGO_DB_NAME]

    # ─── Create Indexes ──────────────────────────────────────────────────
    db.users.create_index("username", unique=True)
    db.users.create_index("email", unique=True)
    db.predictions.create_index("user_id")
    db.predictions.create_index("timestamp")
    db.logs.create_index("timestamp")

    print(f"[DATABASE] Connected to MongoDB: {settings.MONGO_URL}/{settings.MONGO_DB_NAME}")


def close_db():
    """Close the MongoDB connection."""
    global client
    if client:
        client.close()
        print("[DATABASE] MongoDB connection closed.")


def get_db() -> Database:
    """Return the database instance."""
    return db
