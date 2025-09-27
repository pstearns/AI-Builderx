from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..core.settings import get_settings

settings = get_settings()

class Database:
    client: AsyncIOMotorClient = None
    database: AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URI)
    db.database = db.client[settings.DATABASE_NAME]

async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()

def get_database() -> AsyncIOMotorDatabase:
    return db.database
