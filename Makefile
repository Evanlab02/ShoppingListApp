.PHONY: build clean dev down e2e format integration lint migrations pre-test requirements sync-windows test up

build: clean
	python -m build .

clean:
	@rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \
	**/migrations/0*.py \
	.coverage \
	.pytest_cache \
	build/ \
	dist/ \
	*.egg-info

dev:
	python manage.py runserver 0.0.0.0:7001

down:
	docker compose down

e2e: pre-test migrations
	python manage.py populate
	docker compose -f docker-compose.test.yaml up -d --build
	@clear
	pytest -v tests/
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

format:
	black .
	isort . --profile black

integration: pre-test migrations
	python manage.py populate
	docker compose -f docker-compose.test.yaml up -d --build
	@clear
	pytest -v tests/
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

lint: clean
	black --check .
	isort . --check-only --profile black
	flake8 . --max-line-length=100
	pydocstyle .
	mypy . --strict

migrations:
	python manage.py makemigrations
	python manage.py migrate

pre-test:
	@rm -rf shoppingapp/db.sqlite3
	@docker compose down
	@docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

sync-windows:
	rm -rf windows/Pipfile
	cp Pipfile windows/

test: migrations
	pytest -v --ignore=tests/

up:
	docker compose up -d --build
