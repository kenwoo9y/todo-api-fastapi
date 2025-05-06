import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

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
    ASYNC_DB_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
elif DB_TYPE == "postgresql":
    ASYNC_DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
else:
    raise ValueError(f"Unsupported database type: {DB_TYPE}")

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
