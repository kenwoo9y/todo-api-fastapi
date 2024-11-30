from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


class UserBase(BaseModel):
    username: str = Field(..., max_length=30, min_length=3)
    email: EmailStr = Field(..., max_length=80)
    first_name: Optional[str] = Field(None, max_length=40)
    last_name: Optional[str] = Field(None, max_length=40)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    username: Optional[str] = Field(None, max_length=30)
    email: Optional[EmailStr] = Field(None, max_length=80)
    first_name: Optional[str] = Field(None, max_length=40)
    last_name: Optional[str] = Field(None, max_length=40)


class UserResponse(UserBase):
    id: Optional[int] = Field(None)
    created_at: Optional[datetime] = Field(None)
    updated_at: Optional[datetime] = Field(None)


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
