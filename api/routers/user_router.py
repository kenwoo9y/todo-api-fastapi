from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

import api.schemas.user_schema as user_schema
import api.cruds.user_crud as user_crud
from api.db import get_db

router = APIRouter()


@router.post("/users", response_model=user_schema.UserResponse)
async def create(body: user_schema.UserCreate, db: AsyncSession = Depends(get_db)):
    user = await user_crud.create(db=db, user_create=body)
    return user


@router.get("/users/{id}", response_model=Optional[user_schema.UserResponse])
async def get(id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get(db=db, id=id)
    return user


@router.get("/users/username/{user_name}", response_model=Optional[user_schema.UserResponse])
async def get_by_username(user_name: str, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get_by_username(db=db, user_name=user_name)
    return user


@router.get("/users", response_model=List[user_schema.UserResponse], response_model_exclude_unset=True)
async def get_all(db: AsyncSession = Depends(get_db)):
    users = await user_crud.get_all(db=db)
    return users


@router.put("/users/{id}", response_model=user_schema.UserResponse)
async def update(id: int, body: user_schema.UserUpdate, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get(db=db, id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await user_crud.update(db=db, user_update=body, user=user)
    return updated_user


@router.delete("/users/{id}", response_model=None)
async def delete(id: int, db: AsyncSession = Depends(get_db)):
    user = await user_crud.get(db=db, id=id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.delete(db=db, user=user)
