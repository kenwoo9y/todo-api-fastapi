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


def configure_azure_ssl_connection(db_url: str, db_type: str, is_async: bool = False) -> Tuple[str, Dict]:
    """
    Azure環境でのSSL接続設定を適用する。

    Args:
        db_url: データベース接続URL
        db_type: データベースタイプ（'mysql' または 'postgresql'）
        is_async: 非同期エンジンを使用するかどうか

    Returns:
        (修正されたデータベース接続URL, connect_args辞書)のタプル
    """
    import ssl

    connect_args: Dict = {}

    if db_type == "mysql":
        # Azure Database for MySQLはSSL接続が必須
        if is_async:
            # aiomysqlではSSLコンテキストオブジェクトを渡す必要がある
            # 辞書形式では動作しない（uvloopがSSLコンテキストを期待している）
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            connect_args = {
                "ssl": ssl_context,
            }
        else:
            # pymysqlでは辞書形式のSSL設定を使用
            connect_args = {
                "ssl": {
                    "ca": None,  # 証明書検証をスキップ（開発環境用）
                    "check_hostname": False,
                }
            }
    elif db_type == "postgresql":
        # Azure Database for PostgreSQLはSSL接続が必須
        if is_async:
            # asyncpgでSSL接続を有効にするにはURLパラメータにssl=requireを追加
            # asyncpgはsslmodeパラメータをサポートしていない
            parsed = urlparse(db_url)
            query_params = parse_qs(parsed.query)
            if "ssl" not in query_params:
                query_params["ssl"] = ["require"]
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
        else:
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


def apply_azure_ssl_to_url(db_url: str, db_type: str, is_async: bool = True) -> str:
    """
    Azure環境でのSSL接続設定をURLに適用する（URLのみを返す）。

    PostgreSQLの場合:
    - 非同期エンジン（asyncpg）: URLパラメータにssl=requireを追加
    - 同期エンジン（psycopg2）: URLパラメータにsslmode=requireを追加
    MySQLの場合はURLは変更しない（connect_argsで設定する）。

    Args:
        db_url: データベース接続URL
        db_type: データベースタイプ（'mysql' または 'postgresql'）
        is_async: 非同期エンジンを使用するかどうか（デフォルト: True）

    Returns:
        修正されたデータベース接続URL
    """
    parsed = urlparse(db_url)
    query_params = parse_qs(parsed.query)

    if db_type == "postgresql":
        # Azure Database for PostgreSQLはSSL接続が必須
        if is_async:
            # asyncpgでSSL接続を有効にするにはURLパラメータにssl=requireを追加
            # asyncpgはsslmodeパラメータをサポートしていない
            if "ssl" not in query_params:
                query_params["ssl"] = ["require"]
        else:
            # psycopg2でSSL接続を有効にするにはURLパラメータにsslmodeを追加
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


def apply_azure_db_config(db_url: str, is_async: bool = False) -> Tuple[str, Dict]:
    """
    環境変数を確認し、Azure環境の場合はSSL接続設定を適用する。

    Args:
        db_url: データベース接続URL
        is_async: 非同期エンジンを使用するかどうか

    Returns:
        (修正されたデータベース接続URL, connect_args辞書)のタプル
    """
    cloud_provider = os.getenv("CLOUD_PROVIDER", "").lower()
    db_type = os.getenv("DB_TYPE", "").lower()

    if cloud_provider == "azure":
        return configure_azure_ssl_connection(db_url, db_type, is_async)

    return db_url, {}
