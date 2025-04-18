from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

ASYNC_DB_URL = "mysql+aiomysql://root@mysql-db:3306/todo?charset=utf8"
# ASYNC_DB_URL = "postgresql+asyncpg://todo:todo@postgresql-db:5432/todo"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
