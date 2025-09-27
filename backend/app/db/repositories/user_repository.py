from typing import Optional, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.user import User, UserInDB, UserCreate
from ...core.auth import get_password_hash, verify_password

class UserRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.users

    async def create_user(self, user: UserCreate) -> UserInDB:
        """Create a new user"""
        user_dict = user.dict()
        user_dict["password_hash"] = get_password_hash(user.password)
        del user_dict["password"]
        
        result = await self.collection.insert_one(user_dict)
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return UserInDB(**created_user)

    async def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Get user by email"""
        user = await self.collection.find_one({"email": email})
        if user:
            return UserInDB(**user)
        return None

    async def get_user_by_id(self, user_id: ObjectId) -> Optional[UserInDB]:
        """Get user by ID"""
        user = await self.collection.find_one({"_id": user_id})
        if user:
            return UserInDB(**user)
        return None

    async def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticate user with email and password"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    async def create_indexes(self):
        """Create database indexes"""
        await self.collection.create_index("email", unique=True)
