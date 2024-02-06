from fastapi import APIRouter

router = APIRouter()

@router.get("/tasks")
async def show():
    pass

@router.post("/tasks")
async def create():
    pass

@router.put("/tasks/{id}")
async def update():
    pass

@router.delete("/tasks/{id}")
async def delete():
    pass