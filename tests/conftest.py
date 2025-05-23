import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from api.db import Base
from api.db import get_db
from api.main import app

# テスト用のオンメモリSQLiteデータベースURL
ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

# エンジンとセッションの設定
async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)


# テスト用DBセッションを返すfixture
@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # テーブルの初期化
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # FastAPIのDB依存をテスト用にオーバーライド
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db

    # テスト用HTTPクライアント
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    # テスト終了時のリソース解放
    await async_engine.dispose()
