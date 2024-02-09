from fastapi import APIRouter
from typing import List
import api.schemas.task as task_schema

router = APIRouter()

@router.get("/tasks", response_model=List[task_schema.Task])
async def show():
    return [task_schema.Task(id=1, title="ToDo1")]

@router.post("/tasks", response_model=task_schema.TaskCreateResponse)
async def create(task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=1, **task_body.dict())

@router.put("/tasks/{id}", response_model=task_schema.TaskCreateResponse)
async def update(task_id: int, task_body: task_schema.TaskCreate):
    return task_schema.TaskCreateResponse(id=task_id, **task_body.dict())

@router.delete("/tasks/{id}", response_model=None)
async def delete(task_id: int):
    return