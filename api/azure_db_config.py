"""
Azure環境でのデータベース接続設定を提供するモジュール。

Azure Database for MySQL/PostgreSQLはSSL接続が必須のため、
接続URLやconnect_argsを適切に設定する。
"""

import os
from typing import Dict
from typing import Tuple
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urlunparse


def configure_azure_ssl_connection(db_url: str, db_type: str) -> Tuple[str, Dict]:
    """
    Azure環境でのSSL接続設定を適用する。

    Args:
        db_url: データベース接続URL
        db_type: データベースタイプ（'mysql' または 'postgresql'）

    Returns:
        (修正されたデータベース接続URL, connect_args辞書)のタプル
    """
    connect_args: Dict = {}

    if db_type == "mysql":
        # Azure Database for MySQLはSSL接続が必須
        # pymysqlでSSL接続を有効にするにはconnect_argsでSSL設定を渡す
        connect_args = {
            "ssl": {
                "ca": None,  # 証明書検証をスキップ（開発環境用）
                "check_hostname": False,
            }
        }
    elif db_type == "postgresql":
        # Azure Database for PostgreSQLはSSL接続が必須
        # psycopg2でSSL接続を有効にするにはURLパラメータにsslmodeを追加
        parsed = urlparse(db_url)
        query_params = parse_qs(parsed.query)
        query_params["sslmode"] = ["require"]
        new_query = urlencode(query_params, doseq=True)
        db_url = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

    return db_url, connect_args


def apply_azure_ssl_to_url(db_url: str, db_type: str, is_async: bool = False) -> str:
    """
    Azure環境でのSSL接続設定をURLに適用する（URLのみを返す）。

    PostgreSQLの場合はURLパラメータにsslmodeを追加する。
    MySQLの場合:
    - 非同期エンジン（aiomysql）の場合はURLパラメータにssl_disabled=Falseを追加
    - 同期エンジン（pymysql）の場合はURLは変更せずそのまま返す（connect_argsで設定）

    Args:
        db_url: データベース接続URL
        db_type: データベースタイプ（'mysql' または 'postgresql'）
        is_async: 非同期エンジンを使用するかどうか

    Returns:
        修正されたデータベース接続URL
    """
    parsed = urlparse(db_url)
    query_params = parse_qs(parsed.query)

    if db_type == "postgresql":
        # Azure Database for PostgreSQLはSSL接続が必須
        # psycopg2/asyncpgでSSL接続を有効にするにはURLパラメータにsslmodeを追加
        if "sslmode" not in query_params:
            query_params["sslmode"] = ["require"]
    elif db_type == "mysql" and is_async:
        # Azure Database for MySQLはSSL接続が必須
        # aiomysqlでSSL接続を有効にするにはURLパラメータにssl_disabled=Falseを追加
        if "ssl_disabled" not in query_params:
            query_params["ssl_disabled"] = ["False"]
    # MySQLの同期エンジン（pymysql）の場合はURLは変更しない（connect_argsで設定）

    if query_params != parse_qs(parsed.query):
        new_query = urlencode(query_params, doseq=True)
        db_url = urlunparse(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment,
            )
        )

    return db_url


def apply_azure_db_config(db_url: str) -> Tuple[str, Dict]:
    """
    環境変数を確認し、Azure環境の場合はSSL接続設定を適用する。

    Args:
        db_url: データベース接続URL

    Returns:
        (修正されたデータベース接続URL, connect_args辞書)のタプル
    """
    cloud_provider = os.getenv("CLOUD_PROVIDER", "").lower()
    db_type = os.getenv("DB_TYPE", "").lower()

    if cloud_provider == "azure":
        return configure_azure_ssl_connection(db_url, db_type)

    return db_url, {}
