from fastapi import FastAPI

from api.cors import add_cors_middleware
from api.routers import task_router
from api.routers import user_router

app = FastAPI()
app.include_router(task_router.router)
app.include_router(user_router.router)
add_cors_middleware(app=app)
