from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

import api.schemas.user_schema as user_schema
import api.cruds.user_crud as user_crud
from api.db import get_db

router = APIRouter()

@router.post("/users", response_model=user_schema.User)
async def create(
    body: user_schema.UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.create(db=db, user_create=body)
    return user

@router.get("/users/{id}", response_model=Optional[user_schema.User])
async def get(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get(db=db, id=id)
    return user  

@router.get("/users", response_model=List[user_schema.User])
async def get_all(
    db: AsyncSession = Depends(get_db)
):
    users = await user_crud.get_all(db=db)
    return users

@router.put("/users/{id}", response_model=user_schema.User)
async def update(
    id: int,
    body: user_schema.UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.update(db=db, id=id, user_update=body)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@router.delete("/users/{id}", response_model=None)
async def delete(
    id: int,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.delete(db=db, id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")