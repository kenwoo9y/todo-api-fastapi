from datetime import datetime, date
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Status(str, Enum):
    TODO = "ToDo"
    DOING = "Doing"
    DONE = "Done"


class TaskBase(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    due_date: Optional[date] = Field(None)
    status: Optional[Status] = Field(None)
    owner_id: Optional[int] = Field(None)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: Optional[int] = Field(None)
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)


class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
