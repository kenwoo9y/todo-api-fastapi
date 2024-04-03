from datetime import datetime

from typing import Optional
from pydantic import BaseModel, Field

class TaskBase(BaseModel):
   title: str
   description: str
   status: str
   created_at: datetime
   updated_at: datetime

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass
    
class Task(TaskBase):
    id: int
    
    class Config:
        orm_mode = True