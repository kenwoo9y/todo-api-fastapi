from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    id: int
    user_name: str = Field(max_length=30)
    password: str
    email: str = Field(max_length=80)
    last_name: str = Field(max_length=40) 
    first_name: str = Field(max_length=40)
    created_at: datetime
    updated_at: datetime
    