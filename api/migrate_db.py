from urllib.parse import urlparse
from urllib.parse import urlunparse

from dotenv import load_dotenv
from sqlalchemy import create_engine

from api.azure_db_config import apply_azure_db_config
from api.cloud_db_config import get_database_url
from api.models.task_model import Base as TaskBase
from api.models.user_model import Base as UserBase

load_dotenv()


def convert_async_url_to_sync(url: str) -> str:
    """
    非同期データベースURLを同期データベースURLに変換する。

    Args:
        url: 非同期データベース接続URL（例: postgresql+asyncpg://... または mysql+aiomysql://...）

    Returns:
        同期データベース接続URL（例: postgresql+psycopg2://... または mysql+pymysql://...）
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    # 非同期ドライバーを同期ドライバーに置き換え
    if "+asyncpg" in scheme:
        # postgresql+asyncpg -> postgresql+psycopg2
        new_scheme = scheme.replace("+asyncpg", "+psycopg2")
    elif "+aiomysql" in scheme:
        # mysql+aiomysql -> mysql+pymysql
        new_scheme = scheme.replace("+aiomysql", "+pymysql")
    else:
        # 既に同期ドライバーの場合はそのまま返す
        return url

    sync_url = urlunparse((new_scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
    return sync_url


# データベース接続URLを取得（非同期URLを同期URLに変換）
ASYNC_DB_URL = get_database_url()
DB_URL = convert_async_url_to_sync(ASYNC_DB_URL)

# Azure環境の場合、SSL接続設定を適用
DB_URL, connect_args = apply_azure_db_config(DB_URL)

engine = create_engine(DB_URL, echo=True, connect_args=connect_args)


def reset_database():
    TaskBase.metadata.drop_all(bind=engine)
    UserBase.metadata.drop_all(bind=engine)
    TaskBase.metadata.create_all(bind=engine)
    UserBase.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
