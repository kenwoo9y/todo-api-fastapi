from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import api.schemas.user_schema as user_schema
import api.cruds.user_crud as user_crud
from api.db import get_db

router = APIRouter()

@router.post("/users")
async def create():
    pass

@router.get("/users/{id}")
async def get():
    pass

@router.get("/users")
async def get_all():
    pass

@router.put("/users/{id}")
async def update():
    pass

@router.delete("/users/{id}")
async def delete():
    pass