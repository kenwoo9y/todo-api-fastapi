from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.task_schema as task_schema
import api.cruds.task_crud as task_crud
from api.db import get_db

router = APIRouter()

@router.post("/tasks")
async def create():
    pass

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