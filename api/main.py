from fastapi import FastAPI

from api.routers import task_router, user_router

app = FastAPI()
app.include_router(task_router.router)
app.include_router(user_router.router)