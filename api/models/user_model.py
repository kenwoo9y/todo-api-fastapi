from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import relationship

from api.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(30), unique=True, index=True, nullable=False)
    password = Column(Text)
    email = Column(String(80), unique=True, index=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    tasks = relationship("Task", back_populates="owner")
    