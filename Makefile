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
	@python src/manage.py runserver 0.0.0.0:7001 --settings shoppingapp.settings.local_settings

format:
	@black src/
	@isort src/ --profile black

lint:
	@black --check src/
	@isort src/ --check-only --profile black
	@flake8 src/ --max-line-length=100
	@mypy src/ --strict

test:
	@pytest src/ --ignore=src/tests/ -n auto
	@coverage xml
	@coverage html

static:
	@python src/manage.py collectstatic --no-input

clean:
	@rm -rf src/.mypy_cache \
	src/**/__pycache__ \
	src/**/**/__pycache__ \
	src/.coverage \
	src/.pytest_cache \
	src/build/ \
	src/dist/ \
	src/*.egg-info \
	coverage.xml \
	htmlcov \
	src/static
