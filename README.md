# todo-api-fastapi

## セットアップ
### 必要なツール
- Docker & Docker Compose
- Python 3.9
- make コマンド

### 初期設定
1. リポジトリをクローンする。
    ```
    $ git clone https://github.com/kenwoo9y/todo-api-fastapi.git
    $ cd todo-api
    ```

2. 必要なDockerイメージをビルドする。
    ```
    $ make build-local
    ```

3. コンテナを起動する。
    ```
    $ make up
    ```

4. データベースマイグレーションを適用する。  
    使用するDBに応じて`api/migrate_db.py`を編集する。
    ```api/migrate_db.py
    DB_URL = "mysql+pymysql://root@mysql-db:3306/todo?charset=utf8"
    # DB_URL = "postgresql+psycopg2://todo:todo@postgresql-db:5432/todo"
    ```

    ```
    $ make migrate
    ```

5. APIが動作していることを確認する（http://localhost:8000/docs にアクセス）。

## 使用方法
### APIドキュメント
- Swagger UI: http://localhost:8000/docs

### コンテナ管理
- コンテナの状態確認:
    ```
    $ make ps
    ```
- コンテナログの確認:
    ```
    $ make logs
    ```
- コンテナ停止:
    ```
    $ make down
    ```

## 開発
### テストの実行
- テスト実行:
    ```
    $ make test
    ```
- テストカバレッジ:
    ```
    $ make test-coverage
    ```
### コード品質チェック
- Lintチェック:
    ```
    $ make lint-check
    ```
- Lint修正:
    ```
    $ make lint-fix
    ```
- フォーマットチェック:
    ```
    $ make format-check
    ```
- フォーマット修正:
    ```
    $ make format-fix
    ```

## データベース
使用するDBに応じて`api/db.py`を編集する
```api/db.py
ASYNC_DB_URL = "mysql+aiomysql://root@mysql-db:3306/todo?charset=utf8"
# ASYNC_DB_URL = "postgresql+asyncpg://todo:todo@postgresql-db:5432/todo"
```
- MySQLデータベースにアクセス:
    ```
    $ make mysql
    ```
- PostgreSQLデータベースにアクセス:
    ```
    $ make psql
    ```

---
This is a ToDo Web API implemented with FastAPI, designed for simplicity and extensibility.

## Setup
### Setup
- Docker & Docker Compose
- Python 3.9
- `make` command

### Initial Setup
1. Clone this repository:
    ```
    $ git clone https://github.com/kenwoo9y/todo-api-fastapi.git
    $ cd todo-api
    ```

2. Build the required Docker images:
    ```
    $ make build-local
    ```

3. Start the containers:
    ```
    $ make up
    ```

4. Apply database migrations:
    Edit `api/migrate_db.py` based on the database you want to use:
    ```api/migrate_db.py
    DB_URL = "mysql+pymysql://root@mysql-db:3306/todo?charset=utf8"
    # DB_URL = "postgresql+psycopg2://todo:todo@postgresql-db:5432/todo"
    ```
    Then run the migration:
    ```
    $ make migrate
    ```

5. Verify the API is running by accessing http://localhost:8000/docs.

## Usage
### API Documentation
- Swagger UI: http://localhost:8000/docs

### Container Management
- Check container status:
    ```
    $ make ps
    ```
- View container logs:
    ```
    $ make logs
    ```
- Stop containers:
    ```
    $ make down
    ```

## Development
### Running Tests
- Run tests:
    ```
    $ make test
    ```
- Run tests with coverage:
    ```
    $ make test-coverage
    ```
### Code Quality Checks
- Lint check:
    ```
    $ make lint-check
    ```
- Apply lint fixes:
    ```
    $ make lint-fix
    ```
- Check code formatting:
    ```
    $ make format-check
    ```
- Apply code formatting:
    ```
    $ make format-fix
    ```

## Database
Edit `api/db.py` based on the database you want to use:
```api/db.py
ASYNC_DB_URL = "mysql+aiomysql://root@mysql-db:3306/todo?charset=utf8"
# ASYNC_DB_URL = "postgresql+asyncpg://todo:todo@postgresql-db:5432/todo"
```
- Access MySQL database:
    ```
    $ make mysql
    ```
- Access PostgreSQL database:
    ```
    $ make psql
    ```
