# todo-api-fastapi

This is a ToDo Web API implemented with FastAPI, designed for simplicity and extensibility.

## Tech Stack

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00.svg?style=for-the-badge&logo=SQLAlchemy&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Ruff](https://img.shields.io/badge/Ruff-D7FF64.svg?style=for-the-badge&logo=Ruff&logoColor=black)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

### Programming Languages
- [Python](https://www.python.org/) - Primary development language

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) v0.110.1 - High-performance Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) v2.0.29 - SQL toolkit and ORM

### Database
- [MySQL](https://www.mysql.com/) v8.0 - Primary relational database
- [PostgreSQL](https://www.postgresql.org/) v16 - Alternative relational database

### Development Environment
- [Poetry](https://python-poetry.org/) - Python package manager
- [Docker](https://www.docker.com/) - Containerization platform
- [Docker Compose](https://docs.docker.com/compose/) - Tool for defining and running multi-container Docker applications

### Testing & Quality Assurance
- [pytest](https://docs.pytest.org/) v0.23.6 - Python testing framework
- [pytest-cov](https://pytest-cov.readthedocs.io/) v6.0.0 - Code coverage plugin
- [Ruff](https://docs.astral.sh/ruff/) v0.7.4 - Fast Python linter and formatter

### CI/CD
- GitHub Actions - Continuous Integration and Deployment

## Setup
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
