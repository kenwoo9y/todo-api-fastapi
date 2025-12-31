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
    MySQLの場合はURLは変更しない（connect_argsで設定する必要がある）。

    Args:
        db_url: データベース接続URL
        db_type: データベースタイプ（'mysql' または 'postgresql'）
        is_async: 非同期エンジンを使用するかどうか（未使用、将来の拡張用）

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
    # MySQLの場合はURLは変更しない（connect_argsで設定）
    # aiomysqlもpymysqlもURLパラメータではSSL設定できないため

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


def get_azure_async_connect_args(db_type: str) -> Dict:
    """
    Azure環境での非同期エンジン用のconnect_argsを取得する。

    Args:
        db_type: データベースタイプ（'mysql' または 'postgresql'）

    Returns:
        connect_args辞書
    """
    connect_args: Dict = {}

    if db_type == "mysql":
        # Azure Database for MySQLはSSL接続が必須
        # aiomysqlでSSL接続を有効にするにはconnect_argsでssl設定を渡す
        connect_args = {
            "ssl": {
                "ca": None,  # 証明書検証をスキップ（開発環境用）
                "check_hostname": False,
            }
        }
    # PostgreSQLの場合はURLパラメータで設定するため、connect_argsは不要

    return connect_args


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
