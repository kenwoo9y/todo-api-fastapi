from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class Status(str, Enum):
    ToDo = "todo"
    DOING = "doing"
    DONE = "done"

class TaskBase(BaseModel):
   title: Optional[str] = Field(None)
   description: Optional[str] = Field(None)
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
    
    class Config:
        orm_mode = True