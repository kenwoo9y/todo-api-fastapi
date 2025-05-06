.PHONY: help build-local up down logs ps migrate mysql psql test test-coverage lint-check lint-fix format-check format-fix
.DEFAULT_GOAL := help

build-local: ## Build docker image to local development
	docker compose build --no-cache

up: ## Do docker compose up
	docker compose up

down: ## Do docker compose down
	docker compose down

logs: ## Tail docker compose logs
	docker compose logs -f

ps: ## Check container status
	docker compose ps

migrate:  ## Execute migration
	docker-compose exec todo-api poetry run python -m api.migrate_db

mysql: ## Access MySQL Database
	docker compose exec mysql-db mysql -u todo -ptodo

psql: ## Access PostgreSQL Database
	docker compose exec postgresql-db psql -U todo -d todo -W

test: ## Execute tests
	docker-compose run --entrypoint "poetry run pytest -v" todo-api

test-coverage: ## Execute tests with coverage
	docker-compose run --entrypoint "poetry run pytest --cov" todo-api

lint-check: ## Run Ruff linter
	ruff check .

lint-fix: ## Run Ruff linter and apply fixes
	ruff check . --fix

format-check: ## Check code formatting with Ruff
	ruff format . --check --diff

format-fix: ## Format code with Ruff
	ruff format .

help: ## Show options
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'