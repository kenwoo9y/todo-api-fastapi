from fastapi import FastAPI

from api.routers import task_router, user_router
from api.cors import add_cors_middleware

app = FastAPI()
app.include_router(task_router.router)
app.include_router(user_router.router)
add_cors_middleware(app=app)
