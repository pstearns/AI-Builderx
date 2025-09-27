from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from ...models.task import Task, TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db.tasks

    async def create_task(self, task: TaskCreate, user_id: ObjectId) -> Task:
        """Create a new task for a user"""
        task_dict = task.dict()
        task_dict["user_id"] = user_id
        
        result = await self.collection.insert_one(task_dict)
        created_task = await self.collection.find_one({"_id": result.inserted_id})
        return Task(**created_task)

    async def get_tasks_by_user(self, user_id: ObjectId) -> List[Task]:
        """Get all tasks for a user"""
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1)
        tasks = []
        async for task in cursor:
            tasks.append(Task(**task))
        return tasks

    async def get_task_by_id(self, task_id: ObjectId, user_id: ObjectId) -> Optional[Task]:
        """Get a specific task by ID for a user"""
        task = await self.collection.find_one({"_id": task_id, "user_id": user_id})
        if task:
            return Task(**task)
        return None

    async def update_task(self, task_id: ObjectId, user_id: ObjectId, task_update: TaskUpdate) -> Optional[Task]:
        """Update a task"""
        update_data = {k: v for k, v in task_update.dict().items() if v is not None}
        if not update_data:
            return await self.get_task_by_id(task_id, user_id)
        
        update_data["updated_at"] = datetime.utcnow()
        await self.collection.update_one(
            {"_id": task_id, "user_id": user_id},
            {"$set": update_data}
        )
        return await self.get_task_by_id(task_id, user_id)

    async def delete_task(self, task_id: ObjectId, user_id: ObjectId) -> bool:
        """Delete a task"""
        result = await self.collection.delete_one({"_id": task_id, "user_id": user_id})
        return result.deleted_count > 0

    async def get_tasks_by_label(self, user_id: ObjectId, label_id: ObjectId) -> List[Task]:
        """Get tasks that have a specific label"""
        cursor = self.collection.find({"user_id": user_id, "label_ids": label_id}).sort("created_at", -1)
        tasks = []
        async for task in cursor:
            tasks.append(Task(**task))
        return tasks

    async def create_indexes(self):
        """Create database indexes"""
        await self.collection.create_index("user_id")
        await self.collection.create_index("label_ids")
        await self.collection.create_index("deadline")
