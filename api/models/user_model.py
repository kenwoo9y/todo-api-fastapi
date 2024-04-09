from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Text

from api.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(Text)
    email = Column(String(80), unique=True, index=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=False)
    