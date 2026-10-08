from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from pydantic import BaseModel
from typing import Optional, List

# create a simple database with ORM
engine = create_engine("sqlite:///./tasks-simple.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, index=True)

Base.metadata.create_all(bind=engine)


# create simple Pydantic model for task creation
class TaskCreate(BaseModel):
    title: str
    completed: Optional[bool] = False


# create FastAPI app and add CORS middleware
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# define API endpoints for CRUD operations on tasks

@app.get("/api/tasks")
async def read_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    return tasks

@app.post("/api/tasks")
async def create_task(task: TaskCreate):
    db = SessionLocal()
    new_task = Task(title=task.title, completed=task.completed)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/api/tasks/{task_id}")
async def update_task(updated_task: TaskCreate, task_id: int):    
    
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    return {"error": "Task not found"}      

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: int):    
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {"message": "Task deleted"}
    return {"error": "Task not found"}

@app.get("/api/healthcheck")
async def healthcheck():
    return {"status": "ok", "message": "Backend is healthy!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)