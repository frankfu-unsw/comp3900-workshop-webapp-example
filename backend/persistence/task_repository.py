from sqlalchemy.orm import Session
from application.models.task import TaskResponse, TaskCreate
from database.database import TaskDatabase
from typing import List, Optional

class TaskRepository:
    """Repository layer that provides abstracted data access to database"""

    def __init__(self, db: Session):
        self.db_layer = TaskDatabase(db)

    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create a new task"""
        database_response = self.db_layer.create_task(task.title, False)
        return TaskResponse.model_validate(database_response)

    def get_all_tasks(self) -> List[TaskResponse]:
        """Retrieve all tasks"""
        database_responses = self.db_layer.get_all_tasks()
        return [TaskResponse.model_validate(task) for task in database_responses]

    def get_task_by_id(self, task_id: int) -> Optional[TaskResponse]:
        """Get task by ID - returns None if not found"""
        database_response = self.db_layer.get_task_by_id(task_id)
        if not database_response:
            return None
        return TaskResponse.model_validate(database_response)
    

    def update_task(self, task_id: int, title: str = None, completed: bool = None) -> Optional[TaskResponse]:
        """Update a task's title and/or completed status"""
        database_response = self.db_layer.update_task(task_id, title, completed)
        if not database_response:
            return None
        return TaskResponse.model_validate(database_response)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        return self.db_layer.delete_task(task_id)

    def get_completed_tasks(self) -> List[TaskResponse]:
        """Retrieve all completed tasks"""
        return [TaskResponse.model_validate(t) for t in self.db_layer.get_completed_tasks()]

    def get_pending_tasks(self) -> List[TaskResponse]:
        """Retrieve all pending tasks"""
        return [TaskResponse.model_validate(t) for t in self.db_layer.get_pending_tasks()]

    def count_tasks(self) -> int:
        """Count all tasks"""
        return self.db_layer.count_tasks()

    def count_completed_tasks(self) -> int:
        """Count completed tasks"""
        return self.db_layer.count_completed_tasks()

    def count_pending_tasks(self) -> int:
        """Count pending tasks"""
        return self.db_layer.count_pending_tasks()