from sqlalchemy import Column, Integer, String, Boolean
from database.setup import Base


class TaskDatabaseModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, index=False)