from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    user_name: Optional[str] = Field(None)
    email: Optional[EmailStr] = Field(None)
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    
class UserCreate(UserBase):
    password: Optional[str] = Field(None)

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: Optional[int] = Field(None)
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)

class User(UserBase):
    id: int
    
    class Config:
        orm_mode = True