from sqlalchemy.orm import Session
from typing import Optional

from .models.task import TaskDatabaseModel


# Database operations layer
class TaskDatabase:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, title: str, completed: bool = False) -> TaskDatabaseModel:
        """Create a new task in the database"""
        task = TaskDatabaseModel(title=title, completed=completed)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_all_tasks(self) -> list[type[TaskDatabaseModel]]:
        """Retrieve all tasks from the database"""
        return self.db.query(TaskDatabaseModel).all()

    def get_task_by_id(self, task_id: int) -> Optional[TaskDatabaseModel]:
        """Retrieve a specific task by ID"""
        return self.db.query(TaskDatabaseModel).filter(TaskDatabaseModel.id == task_id).first()

    def update_task(self, task_id: int, title: str = None, completed: bool = None) -> Optional[TaskDatabaseModel]:
        """Update a task in the database"""
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        if title is not None:
            task.title = title
        if completed is not None:
            task.completed = completed
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task from the database"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        self.db.delete(task)
        self.db.commit()
        return True

    def get_completed_tasks(self) -> list[type[TaskDatabaseModel]]:
        """Retrieve all completed tasks"""
        return self.db.query(TaskDatabaseModel).filter(TaskDatabaseModel.completed == True).all()

    def get_pending_tasks(self) -> list[type[TaskDatabaseModel]]:
        """Retrieve all pending (incomplete) tasks"""
        return self.db.query(TaskDatabaseModel).filter(TaskDatabaseModel.completed == False).all()

    def count_tasks(self) -> int:
        """Count all tasks"""
        return self.db.query(TaskDatabaseModel).count()

    def count_completed_tasks(self) -> int:
        """Count completed tasks"""
        return self.db.query(TaskDatabaseModel).filter(TaskDatabaseModel.completed == True).count()

    def count_pending_tasks(self) -> int:
        """Count pending tasks"""
        return self.db.query(TaskDatabaseModel).filter(TaskDatabaseModel.completed == False).count()
