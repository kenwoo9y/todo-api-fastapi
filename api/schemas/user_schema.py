from datetime import datetime

from pydantic import BaseModel, Field

class UserBase(BaseModel):
    user_name: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime
    
class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True