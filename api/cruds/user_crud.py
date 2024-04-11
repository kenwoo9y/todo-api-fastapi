from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
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
    result: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == id)
    )
    user = result.first()
    return user[0] if user is not None else None

async def get_by_username(db: AsyncSession, user_name: str):
    result = await db.execute(
        select(user_model.User).filter(user_model.User.user_name == user_name)
    )
    user = result.first()
    return user[0] if user is not None else None

# WIP
async def get_all(db: AsyncSession):
    result: Result = await db.execute(
        select(user_model.User)
    )
    return result.all()

# WIP
async def update(db: AsyncSession, id: int, user_update: user_schema.UserUpdate):
    db_user: Result = await db.execute(
        select(user_model.User).filter(user_model.User.id == id)
    )
    user = db_user.first()
        
    if user:
        user.user_name = user_update.user_name
        user.email = user_update.email
        user.first_name = user_update.first_name
        user.last_name = user_update.last_name
        user.updated_at = user_update.updated_at
        db.add(user)
        
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