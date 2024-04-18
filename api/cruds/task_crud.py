from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import List

import api.models.task_model as task_model
import api.schemas.task_schema as task_schema


async def create(db: AsyncSession, task_create: task_schema.TaskCreate):
    task = task_model.Task(**task_create.dict())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get(db: AsyncSession, id: int):
    async with db.begin():
        result = await db.execute(
            select(task_model.Task).where(task_model.Task.id == id)
        )
        return result.scalars().first()

async def get_all(db: AsyncSession) -> List[task_model.Task]:
    async with db.begin():
        result = await db.execute(
            select(task_model.Task)
        )
        return result.scalars().all()

async def update(db: AsyncSession, id: int, task_update: task_schema.TaskUpdate):
    async with db.begin():
        db_task = await db.execute(
            select(task_model.Task).where(task_model.Task.id == id)
        )
        task = db_task.scalars().first()
        
        if task:
            for key, value in task_update.dict().items():
                setattr(task, key, value)
            await db.commit()
            await db.refresh(task)
            
        return task

async def delete(db: AsyncSession, id: int):
    async with db.begin():
        db_task = await db.execute(
            select(task_model.Task).where(task_model.Task.id == id)
        )
        task = db_task.scalars().first()
        
        if task:
            await db.delete(task)