import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from api.models.task_model import Base as TaskBase
from api.models.user_model import Base as UserBase

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE")
if DB_TYPE is None:
    raise ValueError("DB_TYPE environment variable is not set")

DB_HOST = os.getenv("DB_HOST")
if DB_HOST is None:
    raise ValueError("DB_HOST environment variable is not set")

DB_PORT = os.getenv("DB_PORT")
if DB_PORT is None:
    raise ValueError("DB_PORT environment variable is not set")

DB_NAME = os.getenv("DB_NAME")
if DB_NAME is None:
    raise ValueError("DB_NAME environment variable is not set")

DB_USER = os.getenv("DB_USER")
if DB_USER is None:
    raise ValueError("DB_USER environment variable is not set")

DB_PASSWORD = os.getenv("DB_PASSWORD")
if DB_PASSWORD is None:
    raise ValueError("DB_PASSWORD environment variable is not set")

if DB_TYPE == "mysql":
    DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
elif DB_TYPE == "postgresql":
    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError(f"Unsupported database type: {DB_TYPE}")

engine = create_engine(DB_URL, echo=True)


def reset_database():
    TaskBase.metadata.drop_all(bind=engine)
    UserBase.metadata.drop_all(bind=engine)
    TaskBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
