.PHONY: requirements build up down dev migrate createsuperuser migrations test-migrations format lint test static unit-test test-refresh

IMAGE_NAME = shopping-list-be
VERSION := $(shell cat version.txt)

clean:
	rm -rf static/
	rm -rf .coverage coverage.xml .pytest_cache
	rm -rf **/migrations/0*.py
	rm -rf **/__pycache__/
	rm -rf **/**/__pycache__/
	rm -rf .mypy_cache/

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

up:
	docker compose up -d --build

down:
	docker compose down

dev:
	python manage.py runserver localhost:7000 --settings=shoppingapp.settings.local_settings

migrations:
	python manage.py makemigrations --settings=shoppingapp.settings.local_settings

test-migrations:
	python manage.py makemigrations --settings=shoppingapp.settings.test_settings

migrate: migrations
	python manage.py migrate --settings=shoppingapp.settings.local_settings

createsuperuser:
	python manage.py createsuperuser --settings=shoppingapp.settings.local_settings

format: clean
	black .

lint: clean
	black --check .
	flake8 . --max-line-length=100
	pydocstyle .

unit-test: test-migrations
	pytest -v --cov=. --cov-report term-missing --ignore=tests/

test-auth: test-migrations
	pytest -v authenticationapp/tests/ --cov=authenticationapp/ --cov-report term-missing

static:
	python manage.py collectstatic --noinput --settings=shoppingapp.settings.local_settings

test-refresh:
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

test: test-refresh
	docker compose -f docker-compose.test.yaml up -d --build 
	python manage.py makemigrations --settings=shoppingapp.settings.test_settings
	python manage.py migrate --settings=shoppingapp.settings.test_settings
	pytest -v tests/
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

type-check:
	mypy --strict shoppingapp/