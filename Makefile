.PHONY: clean requirements format lint up down dev migrations

clean:
	@rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \
	**/migrations/0*.py \
	.coverage \
	.pytest_cache

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

format:
	black .
	isort . --profile black

lint: clean
	black --check .
	isort . --check-only --profile black
	flake8 . --max-line-length=100
	pydocstyle .
	mypy . --strict

test: migrations
	pytest --cov=. --cov-report term-missing --ignore=tests/

up:
	docker compose up -d --build

down:
	docker compose down

dev:
	python manage.py runserver 0.0.0.0:7001

migrations:
	python manage.py makemigrations
	python manage.py migrate
