from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import api.schemas.task as task_schema
import api.cruds.task as task_crud
from api.db import get_db

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def show():
    return [task_schema.Task(id=1, title="ToDo1")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create(
    task_body: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create(db, task_body)

@router.put("/tasks/{id}", response_model=task_schema.TaskCreateResponse)
async def update(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

@router.delete("/tasks/{id}", response_model=None)
async def delete(task_id: int):
    return