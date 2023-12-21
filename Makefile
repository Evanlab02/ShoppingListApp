.PHONY: clean requirements format lint up down dev migrations refresh e2e integration test

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
	pytest -v --ignore=tests/

up:
	docker compose up -d --build

down:
	docker compose down

dev:
	python manage.py runserver 0.0.0.0:7001

migrations:
	python manage.py makemigrations
	python manage.py migrate

refresh: down
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

e2e: refresh
	docker compose -f docker-compose.test.yaml up -d --build 
	python manage.py makemigrations
	python manage.py migrate
	pytest -v tests/
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

integration: refresh
	docker compose -f docker-compose.test.yaml up -d --build 
	python manage.py makemigrations
	python manage.py migrate
	pytest -v tests/
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

test-stores: migrations
	pytest stores/

sync-windows:
	rm -rf windows/Pipfile
	cp Pipfile windows/
