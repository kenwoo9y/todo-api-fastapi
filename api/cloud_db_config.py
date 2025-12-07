import os
from urllib.parse import urlparse
from urllib.parse import urlunparse


def normalize_database_url(url: str) -> str:
    """
    データベース接続URLをSQLAlchemyの非同期ドライバー形式に正規化する。

    Args:
        url: データベース接続URL

    Returns:
        正規化されたデータベース接続URL

    Examples:
        - postgres://user:pass@host:5432/db -> postgresql+asyncpg://user:pass@host:5432/db
        - postgresql://user:pass@host:5432/db -> postgresql+asyncpg://user:pass@host:5432/db
        - mysql://user:pass@host:3306/db -> mysql+aiomysql://user:pass@host:3306/db
    """
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()

    # 既に正しい形式の場合はそのまま返す
    if "+asyncpg" in scheme or "+aiomysql" in scheme:
        return url

    # PostgreSQLの正規化
    if scheme in ("postgres", "postgresql"):
        # postgres://またはpostgresql://をpostgresql+asyncpg://に変換
        new_scheme = "postgresql+asyncpg"
        normalized = urlunparse((new_scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
        return normalized

    # MySQLの正規化
    elif scheme == "mysql":
        # mysql://をmysql+aiomysql://に変換
        new_scheme = "mysql+aiomysql"
        # MySQLのデフォルトのcharsetパラメータを追加
        query = parsed.query
        if "charset" not in query:
            query = f"{query}&charset=utf8" if query else "charset=utf8"
        normalized = urlunparse((new_scheme, parsed.netloc, parsed.path, parsed.params, query, parsed.fragment))
        return normalized

    # その他のスキームはそのまま返す（既に正しい形式の可能性がある）
    return url


def get_heroku_database_url() -> str | None:
    """
    Heroku環境のデータベース接続URLを取得する。

    HerokuではDB_TYPE環境変数の値に基づいて以下の環境変数が使用される:
    - DB_TYPE=postgresql: DATABASE_URL（PostgreSQLアドオン用）
    - DB_TYPE=mysql: JAWSDB_URL（MySQLアドオン用）

    Returns:
        正規化されたデータベース接続URL、または環境変数が設定されていない場合はNone
    """
    db_type = os.getenv("DB_TYPE")

    if db_type is None:
        return None

    db_type_lower = db_type.lower()

    if db_type_lower == "postgresql":
        # PostgreSQLの場合はDATABASE_URLを使用
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    elif db_type_lower == "mysql":
        # MySQLの場合はJAWSDB_URLを使用
        jawsdb_url = os.getenv("JAWSDB_URL")
        if jawsdb_url:
            return normalize_database_url(jawsdb_url)

    return None


def get_aws_database_url() -> str | None:
    """
    AWS環境のデータベース接続URLを取得する。

    AWSではDB_TYPE環境変数の値に基づいて以下の環境変数が使用される:
    - DB_TYPE=postgresql: POSTGRESQL_DATABASE_URL
    - DB_TYPE=mysql: MYSQL_DATABASE_URL

    Returns:
        正規化されたデータベース接続URL、または環境変数が設定されていない場合はNone
    """
    db_type = os.getenv("DB_TYPE")

    if db_type is None:
        return None

    db_type_lower = db_type.lower()

    if db_type_lower == "postgresql":
        # PostgreSQLの場合はPOSTGRESQL_DATABASE_URLを使用
        database_url = os.getenv("POSTGRESQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    elif db_type_lower == "mysql":
        # MySQLの場合はMYSQL_DATABASE_URLを使用
        database_url = os.getenv("MYSQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    return None


def get_gcp_database_url() -> str | None:
    """
    Google Cloud Platform環境のデータベース接続URLを取得する。

    GCPではDB_TYPE環境変数の値に基づいて以下の環境変数が使用される:
    - DB_TYPE=postgresql: POSTGRESQL_DATABASE_URL
    - DB_TYPE=mysql: MYSQL_DATABASE_URL

    Returns:
        正規化されたデータベース接続URL、または環境変数が設定されていない場合はNone
    """
    db_type = os.getenv("DB_TYPE")

    if db_type is None:
        return None

    db_type_lower = db_type.lower()

    if db_type_lower == "postgresql":
        # PostgreSQLの場合はPOSTGRESQL_DATABASE_URLを使用
        database_url = os.getenv("POSTGRESQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    elif db_type_lower == "mysql":
        # MySQLの場合はMYSQL_DATABASE_URLを使用
        database_url = os.getenv("MYSQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    return None


def get_azure_database_url() -> str | None:
    """
    Azure環境のデータベース接続URLを取得する。

    AzureではDB_TYPE環境変数の値に基づいて以下の環境変数が使用される:
    - DB_TYPE=postgresql: POSTGRESQL_DATABASE_URL
    - DB_TYPE=mysql: MYSQL_DATABASE_URL

    Returns:
        正規化されたデータベース接続URL、または環境変数が設定されていない場合はNone
    """
    db_type = os.getenv("DB_TYPE")

    if db_type is None:
        return None

    db_type_lower = db_type.lower()

    if db_type_lower == "postgresql":
        # PostgreSQLの場合はPOSTGRESQL_DATABASE_URLを使用
        database_url = os.getenv("POSTGRESQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    elif db_type_lower == "mysql":
        # MySQLの場合はMYSQL_DATABASE_URLを使用
        database_url = os.getenv("MYSQL_DATABASE_URL")
        if database_url:
            return normalize_database_url(database_url)

    return None


def get_local_database_url() -> str | None:
    """
    ローカル環境のデータベース接続URLを取得する。

    ローカル環境では個別の環境変数（DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD）
    から接続URLを構築する。

    Returns:
        正規化されたデータベース接続URL、または環境変数が設定されていない場合はNone
    """
    # 個別の環境変数がすべて設定されている場合のみ構築
    if all(os.getenv(key) for key in ["DB_TYPE", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]):
        database_url = _build_database_url_from_env()
        return normalize_database_url(database_url)

    return None


def _build_database_url_from_env() -> str:
    """
    環境変数からデータベース接続URLを構築する（内部関数）。

    Returns:
        データベース接続URL

    Raises:
        ValueError: 必要な環境変数が設定されていない場合
    """
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
        return f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8"
    elif DB_TYPE == "postgresql":
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    else:
        raise ValueError(f"Unsupported database type: {DB_TYPE}. Use 'mysql' or 'postgresql'.")


def get_database_url() -> str:
    """
    環境変数からデータベース接続URLを取得する。

    CLOUD_PROVIDER環境変数に基づいて、対応するクラウドサービスの関数を呼び出す。

    対応する値:
    - Heroku: Heroku環境（DB_TYPE=postgresqlならDATABASE_URL、DB_TYPE=mysqlならJAWSDB_URL）
    - AWS: AWS環境（DB_TYPE=postgresqlならPOSTGRESQL_DATABASE_URL、DB_TYPE=mysqlならMYSQL_DATABASE_URL）
    - GCP: Google Cloud環境（DB_TYPE=postgresqlならPOSTGRESQL_DATABASE_URL、DB_TYPE=mysqlならMYSQL_DATABASE_URL）
    - Azure: Azure環境（DB_TYPE=postgresqlならPOSTGRESQL_DATABASE_URL、DB_TYPE=mysqlならMYSQL_DATABASE_URL）
    - 環境変数が存在しない場合: ローカル環境（個別環境変数）

    Returns:
        正規化されたデータベース接続URL

    Raises:
        ValueError: データベース接続情報が設定されていない場合、または無効なCLOUD_PROVIDER値が設定されている場合
    """
    # CLOUD_PROVIDER環境変数を取得（大文字小文字を区別しない）
    cloud_provider = os.getenv("CLOUD_PROVIDER")

    if cloud_provider is None:
        # 環境変数が存在しない場合はローカル環境として扱う
        database_url = get_local_database_url()
        if database_url:
            return database_url
        raise ValueError(
            "Database connection URL not found for local environment. "
            "Please set individual environment variables: DB_TYPE, DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD"
        )

    # 大文字小文字を区別しない比較のため、小文字に変換
    cloud_provider_lower = cloud_provider.lower()

    # クラウドプロバイダーに応じた関数を呼び出す
    provider_map = {
        "heroku": get_heroku_database_url,
        "aws": get_aws_database_url,
        "gcp": get_gcp_database_url,
        "azure": get_azure_database_url,
    }

    provider_func = provider_map.get(cloud_provider_lower)

    if provider_func is None:
        valid_providers = ", ".join(provider_map.keys())
        raise ValueError(
            f"Invalid CLOUD_PROVIDER value: {cloud_provider}. "
            f"Valid values are: {valid_providers}, or leave unset for local environment."
        )

    # 対応するプロバイダーの関数を呼び出す
    database_url = provider_func()

    if database_url is None:
        provider_name = cloud_provider.capitalize()

        # Herokuの場合は特別なメッセージ
        if cloud_provider_lower == "heroku":
            raise ValueError(
                f"Database connection URL not found for {provider_name} environment. "
                "Please set the following:\n"
                "- DB_TYPE=postgresql and DATABASE_URL (for Heroku PostgreSQL)\n"
                "- DB_TYPE=mysql and JAWSDB_URL (for Heroku MySQL)"
            )

        # AWS、GCP、Azureの場合はDB_TYPEに応じた環境変数
        raise ValueError(
            f"Database connection URL not found for {provider_name} environment. "
            "Please set the following:\n"
            "- DB_TYPE=postgresql and POSTGRESQL_DATABASE_URL (for PostgreSQL)\n"
            "- DB_TYPE=mysql and MYSQL_DATABASE_URL (for MySQL)"
        )

    return database_url
