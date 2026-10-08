from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.setup import get_db
from application.task_service import TaskService
from application.models.task import TaskCreate, TaskResponse
from typing import List

from persistence.task_repository import TaskRepository

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    service = TaskService(task_repository)
    return service.create_task(task)

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    service = TaskService(task_repository)
    return service.get_all_tasks()

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    service = TaskService(task_repository)
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    task_repository = TaskRepository(db)
    service = TaskService(task_repository)
    try:
        updated_task = service.update_task(task_id, title=task_update.title, completed=task_update.completed)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return updated_task    