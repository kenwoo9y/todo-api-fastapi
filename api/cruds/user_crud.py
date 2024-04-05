from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List

import api.models.user_model as user_model
import api.schemas.user_schema as user_schema

async def create(db: AsyncSession, user_create: user_schema.UserCreate):
    user = user_model.User(**user_create.dict())
    db.add(user)
    
    await db.commit()
    await db.refresh(user)
    return user

async def get(db: AsyncSession, id: int):
    async with db.begin():
        result = await db.execute(
            select(user_model.User).where(user_model.User.id == id)
        )
        return result.scalars().first()

async def get_by_username(db: AsyncSession, user_name: str):
    async with db.begin():
        result = await db.execute(
            select(user_model.User).where(user_model.User.user_name == user_name)
        )
        return result.scalars().first()

async def get_all(db: AsyncSession) -> List[user_model.User]:
    async with db.begin():
        result = await db.execute(
            select(user_model.User)
        )
        return result.scalars().all()

async def update(db: AsyncSession, id: int, user_update: user_schema.UserUpdate):
    async with db.begin():
        db_user = await db.execute(
            select(user_model.User).where(user_model.User.id == id)
        )
        user = db_user.scalars().first()
        
        if user:
            for key, value in user_update.dict().items():
                setattr(user, key, value)
            await db.commit()
            await db.refresh(user)
            
        return user

async def delete(db: AsyncSession, id: int):
    async with db.begin():
        db_user = await db.execute(
            select(user_model.User).where(user_model.User.id == id)
        )
        user = db_user.scalars().first()
        
        if user:
            await db.delete(user)