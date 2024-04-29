.PHONY: help build-local up down logs ps test migrate mysql psql 
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

test: # Execute tests
	docker-compose run --entrypoint "poetry run pytest" todo-api

migrate:  ## Execute migration
	docker-compose exec todo-api poetry run python -m ./api.migrate_db

mysql: ## Access MySQL Database
	docker-compose exec mysql-db mysql todo

psql: ## Access PostgreSQL Database
	docker-compose exec postgresql-db psql -U todo

help: ## Show options
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'