from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def show():
    return [task_schema.Task(id=1, title="ToDo1")]

@router.post("/tasks")
async def create():
    pass

@router.put("/tasks/{id}")
async def update():
    pass

@router.delete("/tasks/{id}")
async def delete():
    pass