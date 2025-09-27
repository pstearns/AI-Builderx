from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Complete project documentation")
    description: Optional[str] = Field(None, max_length=1000, example="Write comprehensive documentation for the TODO API")
    priority: str = Field(..., pattern="^(High|Medium|Low)$", example="High")
    deadline: date = Field(..., example="2024-12-31")
    status: str = Field(default="open", pattern="^(open|done)$", example="open")

class TaskCreate(TaskBase):
    label_ids: List[PyObjectId] = Field(default_factory=list)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[str] = Field(None, pattern="^(High|Medium|Low)$")
    deadline: Optional[date] = None
    status: Optional[str] = Field(None, pattern="^(open|done)$")
    label_ids: Optional[List[PyObjectId]] = None

class Task(TaskBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    label_ids: List[PyObjectId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
