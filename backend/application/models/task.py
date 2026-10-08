from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    # Allows us to create Pydantic models directly from ORM objects
    class Config:
        from_attributes = True