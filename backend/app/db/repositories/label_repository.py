from typing import List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.label import Label, LabelCreate, LabelUpdate

class LabelRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.labels

    async def create_label(self, label: LabelCreate, user_id: ObjectId) -> Label:
        """Create a new label for a user"""
        label_dict = label.dict()
        label_dict["user_id"] = user_id
        
        result = await self.collection.insert_one(label_dict)
        created_label = await self.collection.find_one({"_id": result.inserted_id})
        return Label(**created_label)

    async def get_labels_by_user(self, user_id: ObjectId) -> List[Label]:
        """Get all labels for a user"""
        cursor = self.collection.find({"user_id": user_id})
        labels = []
        async for label in cursor:
            labels.append(Label(**label))
        return labels

    async def get_label_by_id(self, label_id: ObjectId, user_id: ObjectId) -> Optional[Label]:
        """Get a specific label by ID for a user"""
        label = await self.collection.find_one({"_id": label_id, "user_id": user_id})
        if label:
            return Label(**label)
        return None

    async def update_label(self, label_id: ObjectId, user_id: ObjectId, label_update: LabelUpdate) -> Optional[Label]:
        """Update a label"""
        update_data = {k: v for k, v in label_update.dict().items() if v is not None}
        if not update_data:
            return await self.get_label_by_id(label_id, user_id)
        
        update_data["updated_at"] = label_update.updated_at
        await self.collection.update_one(
            {"_id": label_id, "user_id": user_id},
            {"$set": update_data}
        )
        return await self.get_label_by_id(label_id, user_id)

    async def delete_label(self, label_id: ObjectId, user_id: ObjectId) -> bool:
        """Delete a label"""
        result = await self.collection.delete_one({"_id": label_id, "user_id": user_id})
        return result.deleted_count > 0

    async def create_indexes(self):
        """Create database indexes"""
        await self.collection.create_index([("user_id", 1), ("name", 1)], unique=True)
