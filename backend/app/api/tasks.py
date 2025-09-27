from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from bson import ObjectId
from ..core.dependencies import get_current_user
from ..db.database import get_database
from ..db.repositories.task_repository import TaskRepository
from ..db.repositories.label_repository import LabelRepository
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import UserInDB

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[Task])
async def get_tasks(current_user: UserInDB = Depends(get_current_user)):
    """Get all tasks for the current user"""
    db = get_database()
    task_repo = TaskRepository(db)
    return await task_repo.get_tasks_by_user(current_user.id)

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: TaskCreate, 
    current_user: UserInDB = Depends(get_current_user)
):
    """Create a new task"""
    db = get_database()
    task_repo = TaskRepository(db)
    label_repo = LabelRepository(db)
    
    # Validate that all label_ids belong to the current user
    if task.label_ids:
        for label_id in task.label_ids:
            label = await label_repo.get_label_by_id(label_id, current_user.id)
            if not label:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Label with id {label_id} not found or does not belong to user"
                )
    
    return await task_repo.create_task(task, current_user.id)

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: str, 
    current_user: UserInDB = Depends(get_current_user)
):
    """Get a specific task by ID"""
    db = get_database()
    task_repo = TaskRepository(db)
    
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    task = await task_repo.get_task_by_id(task_object_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserInDB = Depends(get_current_user)
):
    """Update a task"""
    db = get_database()
    task_repo = TaskRepository(db)
    label_repo = LabelRepository(db)
    
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    # Validate that all label_ids belong to the current user
    if task_update.label_ids:
        for label_id in task_update.label_ids:
            label = await label_repo.get_label_by_id(label_id, current_user.id)
            if not label:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Label with id {label_id} not found or does not belong to user"
                )
    
    task = await task_repo.update_task(task_object_id, current_user.id, task_update)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Delete a task"""
    db = get_database()
    task_repo = TaskRepository(db)
    
    try:
        task_object_id = ObjectId(task_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid task ID format"
        )
    
    success = await task_repo.delete_task(task_object_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

@router.get("/by-label/{label_id}", response_model=List[Task])
async def get_tasks_by_label(
    label_id: str,
    current_user: UserInDB = Depends(get_current_user)
):
    """Get tasks that have a specific label"""
    db = get_database()
    task_repo = TaskRepository(db)
    label_repo = LabelRepository(db)
    
    try:
        label_object_id = ObjectId(label_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid label ID format"
        )
    
    # Verify label belongs to user
    label = await label_repo.get_label_by_id(label_object_id, current_user.id)
    if not label:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Label not found"
        )
    
    return await task_repo.get_tasks_by_label(current_user.id, label_object_id)
