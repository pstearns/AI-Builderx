from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from .user import PyObjectId

class LabelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, example="Work")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", example="#FF5733")

class LabelCreate(LabelBase):
    pass

class LabelUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50, example="Personal")
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$", example="#33FF57")

class Label(LabelBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str}
    }
