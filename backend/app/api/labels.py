from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from ..core.dependencies import get_current_user
from ..db.database import get_database
from ..db.repositories.label_repository import LabelRepository
from ..models.label import Label, LabelCreate, LabelUpdate
from ..models.user import UserInDB

router = APIRouter(prefix="/labels", tags=["labels"])

@router.get("/", response_model=List[Label])
async def get_labels(current_user: UserInDB = Depends(get_current_user)):
    """Get all labels for the current user"""
    db = get_database()
    label_repo = LabelRepository(db)
    return await label_repo.get_labels_by_user(current_user.id)

@router.post("/", response_model=Label, status_code=status.HTTP_201_CREATED)
async def create_label(
    label: LabelCreate, 
    current_user: UserInDB = Depends(get_current_user)
):
    """Create a new label"""
    db = get_database()
    label_repo = LabelRepository(db)
    
    try:
        return await label_repo.create_label(label, current_user.id)
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A label with this name already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create label"
        )

@router.get("/{label_id}", response_model=Label)
async def get_label(
    label_id: str, 
    current_user: UserInDB = Depends(get_current_user)
):
    """Get a specific label by ID"""
    db = get_database()
    label_repo = LabelRepository(db)
    
    try:
        label_object_id = ObjectId(label_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID format"
        )
    
    label = await label_repo.get_label_by_id(label_object_id, current_user.id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    return label

@router.put("/{label_id}", response_model=Label)
async def update_label(
    label_id: str,
    label_update: LabelUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update a label"""
    db = get_database()
    label_repo = LabelRepository(db)
    
    try:
        label_object_id = ObjectId(label_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID format"
        )
    
    try:
        label = await label_repo.update_label(label_object_id, current_user.id, label_update)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found"
            )
        return label
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A label with this name already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update label"
        )

@router.delete("/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_label(
    label_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Delete a label"""
    db = get_database()
    label_repo = LabelRepository(db)
    
    try:
        label_object_id = ObjectId(label_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID format"
        )
    
    success = await label_repo.delete_label(label_object_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
