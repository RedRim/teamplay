include .env

database_name = db
DOCKER_COMP = docker compose -f docker-compose.yml
NAME = backend
EXEC = $(DOCKER_COMP) exec $(NAME)

POSTGRES_CONT = $(DOCKER_COMP) exec db
BACKEND_CONT = $(DOCKER_COMP) exec backend

build:
	$(DOCKER_COMP) build --pull --no-cache

up:
	@$(DOCKER_COMP) up --detach --wait

down:
	@$(DOCKER_COMP) down --remove-orphans

full-restart: down up

postgres:
	@$(POSTGRES_CONT) psql -U postgres -w postgres -d $(database_name)

download-dump:
	@echo "Dumping to $(name)..."
	@$(POSTGRES_CONT) pg_dump -U postgres -Fc $(database_name) > $(name)

upload-dump:
	@echo "Recreating '$(database_name)' database..."
	@$(POSTGRES_CONT) psql -U postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$(database_name)';"
	@$(POSTGRES_CONT) psql -U postgres -c "DROP DATABASE IF EXISTS $(database_name);"
	@$(POSTGRES_CONT) psql -U postgres -c "CREATE DATABASE $(database_name);"
	@echo "Applying $(name) dump..."
	@$(POSTGRES_CONT) bash -c "pg_restore -e -v -U postgres -Fc --no-owner --no-privileges -d $(database_name) /dump/$(name)"


# ---------- Alembic MIGRATIONS ----------
init-alembic:
	@$(BACKEND_CONT) alembic init -t async migration

makemigrations:
	@$(BACKEND_CONT) alembic revision --autogenerate -m $(name)

migrate:
	@$(BACKEND_CONT) alembic upgrade head

downgrade:
	@$(BACKEND_CONT) alembic downgrade $(name)

alembic-merge:
	@$(BACKEND_CONT) alembic merge heads -m ${name}