from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.user_model as user_model
import api.schemas.user_schema as user_schema


async def create(db: AsyncSession, user_create: user_schema.UserCreate):
    user = user_model.User(**user_create.model_dump())
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
    except IntegrityError as error:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Username already exists") from error
    return user


async def get(db: AsyncSession, id: int):
    result: Result = await db.execute(select(user_model.User).filter(user_model.User.id == id))
    user = result.first()
    return user[0] if user is not None else None


async def get_by_username(db: AsyncSession, username: str):
    result: Result = await db.execute(select(user_model.User).filter(user_model.User.username == username))
    user = result.first()
    return user[0] if user is not None else None


async def get_all(db: AsyncSession):
    result: Result = await db.execute(select(user_model.User))
    return result.scalars().all()


async def update(db: AsyncSession, user_update: user_schema.UserUpdate, user: user_model.User):
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def delete(db: AsyncSession, user: user_model.User):
    await db.delete(user)
    await db.commit()
