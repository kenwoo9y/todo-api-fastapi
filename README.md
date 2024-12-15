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
