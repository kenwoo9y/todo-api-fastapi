from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select

from typing import List

import api.models.task_model as task_model
import api.schemas.task_schema as task_schema

async def create(db: AsyncSession, task_create: task_schema.TaskCreate):
    task = task_model.Task(**task_create.model_dump())
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get(db: AsyncSession, id: int):
    result: Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.id == id)
    )
    task = result.first()
    return task[0] if task is not None else None

async def get_all(db: AsyncSession):
    result:Result = await db.execute(
        select(task_model.Task)
    )
    return result.scalars().all()

async def get_all_by_owner(db: AsyncSession, owner_id: int):
    result:Result = await db.execute(
        select(task_model.Task).filter(task_model.Task.owner_id == owner_id)
    )
    return result.scalars().all()

async def update(db: AsyncSession, task_update: task_schema.TaskUpdate, task: task_model.Task):
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def delete(db: AsyncSession, task: task_model.Task):
    await db.delete(task)
    await db.commit()