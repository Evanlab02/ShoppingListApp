.PHONY: install debug build up down requirements clean run format lint static test

debug:
	@docker compose -f docker/docker-compose.yaml up

build:
	@docker compose -f docker/docker-compose.yaml build

up:
	@docker compose -f docker/docker-compose.yaml up -d

down:
	@docker compose -f docker/docker-compose.yaml down

requirements:
	@pipenv requirements > requirements.txt
	@pipenv requirements --dev > requirements-dev.txt

run:
	@python manage.py runserver 0.0.0.0:7001 --settings shoppingapp.settings.local_settings

format:
	@black .
	@isort . --profile black

lint:
	@black --check .
	@isort . --check-only --profile black
	@flake8 . --max-line-length=100
	@mypy . --strict

test:
	@pytest . -n auto
	@coverage xml
	@coverage html

static:
	@python manage.py collectstatic --no-input

clean:
	@rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \
	.coverage \
	.pytest_cache \
	build/ \
	dist/ \
	*.egg-info \
	coverage.xml \
	htmlcov \
