from typing import List
from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task_crud as task_crud
import api.schemas.task_schema as task_schema
from api.db import get_db

router = APIRouter()


@router.post("/tasks", response_model=task_schema.TaskResponse, status_code=201)
async def create_task(body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await task_crud.create(db=db, task_create=body)
    return task


@router.get("/tasks/{id}", response_model=Optional[task_schema.TaskResponse])
async def get_task(id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db=db, id=id)
    return task


@router.get("/tasks", response_model=List[task_schema.TaskResponse], response_model_exclude_unset=True)
async def get_all_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await task_crud.get_all(db=db)
    return tasks


@router.get("/users/{owner_id}/tasks", response_model=List[task_schema.TaskResponse], response_model_exclude_unset=True)
async def get_all_tasks_by_owner(owner_id: int, db: AsyncSession = Depends(get_db)):
    tasks = await task_crud.get_all_by_owner(db=db, owner_id=owner_id)
    return tasks


@router.patch("/tasks/{id}", response_model=task_schema.TaskResponse)
async def update_task(id: int, body: task_schema.TaskUpdate, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db=db, id=id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updated_task = await task_crud.update(db=db, task_update=body, task=task)
    return updated_task


@router.delete("/tasks/{id}", response_model=None)
async def delete_task(id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get(db=db, id=id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete(db=db, task=task)
