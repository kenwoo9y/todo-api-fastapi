from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.task_schema as task_schema
import api.cruds.task_crud as task_crud
from api.db import get_db

router = APIRouter()

@router.post("/tasks", response_model=task_schema.TaskResponse)
async def create(
    body: task_schema.TaskCreate,
    db: AsyncSession = Depends(get_db)
):
    task = await task_crud.create(db=db, task_create=body)
    return task

@router.get("/tasks")
async def get():
    pass

@router.get("/tasks")
async def get_all():
    pass

@router.put("/tasks/{id}")
async def update():
    pass

@router.delete("/tasks/{id}")
async def delete():
    pass