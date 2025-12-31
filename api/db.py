import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from api.azure_db_config import get_azure_async_connect_args
from api.cloud_db_config import get_database_url

load_dotenv()


# データベース接続URLを取得
ASYNC_DB_URL = get_database_url()

# Azure環境の場合、非同期エンジン用のconnect_argsを取得
connect_args = {}
cloud_provider = os.getenv("CLOUD_PROVIDER", "").lower()
db_type = os.getenv("DB_TYPE", "").lower()

if cloud_provider == "azure":
    connect_args = get_azure_async_connect_args(db_type)

async_engine = create_async_engine(ASYNC_DB_URL, echo=True, connect_args=connect_args)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
