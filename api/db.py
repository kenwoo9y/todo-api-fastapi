
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from api.azure_db_config import apply_azure_db_config
from api.cloud_db_config import get_database_url

load_dotenv()


# データベース接続URLを取得
ASYNC_DB_URL = get_database_url()

# Azure環境の場合、SSL接続設定を適用
ASYNC_DB_URL, connect_args = apply_azure_db_config(ASYNC_DB_URL)

async_engine = create_async_engine(ASYNC_DB_URL, echo=True, connect_args=connect_args)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
