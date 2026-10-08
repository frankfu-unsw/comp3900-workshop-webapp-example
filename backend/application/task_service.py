from application.models.task import TaskCreate, TaskResponse
from persistence.task_repository import TaskRepository
from typing import List, Optional

class TaskService:
    """Service layer that contains business logic and coordinates repository operations"""

    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def create_task(self, task: TaskCreate) -> TaskResponse:
        """Create a new task with business validation"""
        # Business validation
        if not task.title or not task.title.strip():
            raise ValueError("Task title cannot be empty")

        title = task.title.strip()
        return self.task_repository.create_task(task)

    def get_all_tasks(self) -> List[TaskResponse]:
        """Retrieve all tasks"""
        return self.task_repository.get_all_tasks()

    def get_task_by_id(self, task_id: int) -> TaskResponse:
        """Get task by ID with business validation"""
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        task = self.task_repository.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        return task

    def update_task(self, task_id: int, title: str = None, completed: bool = None) -> TaskResponse:
        """Update a task with business validation"""
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        if title is not None:
            if not title or not title.strip():
                raise ValueError("Task title cannot be empty")
            title = title.strip()

        updated_task = self.task_repository.update_task(task_id, title, completed)
        if not updated_task:
            raise ValueError(f"Task with ID {task_id} not found")

        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task with validation"""
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")

        # Check if task exists before attempting deletion
        existing_task = self.task_repository.get_task_by_id(task_id)
        if not existing_task:
            raise ValueError(f"Task with ID {task_id} not found")

        return self.task_repository.delete_task(task_id)

    def mark_task_completed(self, task_id: int) -> TaskResponse:
        """Mark a task as completed"""
        return self.update_task(task_id, completed=True)

    def mark_task_pending(self, task_id: int) -> TaskResponse:
        """Mark a task as pending"""
        return self.update_task(task_id, completed=False)

    def toggle_task_status(self, task_id: int) -> TaskResponse:
        """Toggle the completion status of a task"""
        task = self.get_task_by_id(task_id)  # This handles validation and not found cases
        return self.update_task(task_id, completed=not task.completed)

    def get_completed_tasks(self) -> List[TaskResponse]:
        """Get all completed tasks"""
        return self.task_repository.get_completed_tasks()

    def get_pending_tasks(self) -> List[TaskResponse]:
        """Get all pending tasks"""
        return self.task_repository.get_pending_tasks()

    def get_task_statistics(self) -> dict:
        """Get statistics about tasks - business logic for aggregating data"""
        total = self.task_repository.count_tasks()
        completed = self.task_repository.count_completed_tasks()
        pending = self.task_repository.count_pending_tasks()

        return {
            "total_tasks": total,
            "completed_tasks": completed,
            "pending_tasks": pending,
            "completion_rate": (completed / total * 100) if total > 0 else 0
        }

    def bulk_mark_completed(self, task_ids: List[int]) -> List[TaskResponse]:
        """Business logic for bulk operations"""
        updated_tasks = []
        for task_id in task_ids:
            try:
                updated_task = self.mark_task_completed(task_id)
                updated_tasks.append(updated_task)
            except ValueError:
                # Skip invalid task IDs, or you could collect errors and return them
                continue
        return updated_tasks

    def get_task_summary(self) -> dict:
        """Business logic for creating task summaries"""
        stats = self.get_task_statistics()
        recent_tasks = self.get_all_tasks()[-5:]  # Last 5 tasks as example

        return {
            "statistics": stats,
            "recent_tasks": recent_tasks,
            "has_pending_tasks": stats["pending_tasks"] > 0
        }