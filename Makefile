.PHONY: requirements build up down dev migrate createsuperuser

IMAGE_NAME = shopping-list-be
VERSION := $(shell cat version.txt)

clean:
	rm -rf .coverage coverage.xml .pytest_cache
	rm -rf **/migrations/0*.py

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

migrate:
	python manage.py makemigrations --settings=shoppingapp.settings.local_settings
	python manage.py migrate --settings=shoppingapp.settings.local_settings

createsuperuser:
	python manage.py createsuperuser --settings=shoppingapp.settings.local_settings

format: clean
	black .

lint: clean
	black --check .
	flake8 . --max-line-length=100
	pydocstyle .

test:
	python manage.py makemigrations --settings=shoppingapp.settings.test_settings
	pytest -v --cov=. --cov-report term-missing
