from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from api.cloud_db_config import get_database_url

load_dotenv()


# データベース接続URLを取得
ASYNC_DB_URL = get_database_url()

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
