.PHONY: local-dev local acceptance e2e up up-build up-debug down int int-build int-debug int-down int-setup dev clean build format lint migrations requirements

local-dev:
	@python manage.py makemigrations
	@python manage.py migrate
	@python manage.py runserver 0.0.0.0:7001 --settings shoppingapp.settings.local_settings

local:
	@python manage.py makemigrations
	@python manage.py migrate
	@python -m shoppingapp.config.local_config

acceptance:
	@docker compose down
	@docker compose -f docker-compose.test.yaml down --remove-orphans --volumes
	@docker compose -f docker-compose.test.yaml up -d --build
	@docker exec test-shopping-app-be python manage.py makemigrations
	@docker exec test-shopping-app-be python manage.py migrate
	@docker exec test-shopping-app-be python manage.py populate
	@clear
	pytest tests/ -v
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

e2e:
	@docker compose down
	@docker compose -f docker-compose.test.yaml down --remove-orphans --volumes
	@docker compose -f docker-compose.test.yaml up -d --build
	@docker exec test-shopping-app-be python manage.py makemigrations
	@docker exec test-shopping-app-be python manage.py migrate
	@docker exec test-shopping-app-be python manage.py populate
	@clear
	pytest tests/ -v
	docker compose -f docker-compose.test.yaml down --remove-orphans --volumes

up:
	docker compose up -d

up-build:
	docker compose build

up-debug:
	docker compose up

down:
	docker compose down

int:
	docker compose -f docker-compose.int.yaml up -d

int-build:
	docker compose -f docker-compose.int.yaml build

int-debug:
	docker compose -f docker-compose.int.yaml up

int-down:
	docker compose -f docker-compose.int.yaml down

int-setup:
	docker exec shopping-django-app python manage.py makemigrations
	docker exec shopping-django-app python manage.py migrate
	docker exec -it shopping-django-app bash
	docker exec shopping-django-app python manage.py collectstatic --noinput
	docker exec shopping-django-app rm -rf manage.py
	docker cp shopping-django-app:/app/static/ ./static/
	docker cp ./static/ shopping-app:/var/www/html/static/
	rm -rf ./static/
	docker restart shopping-django-app
	docker restart shopping-app

int-refresh:
	docker exec shopping-django-app python manage.py collectstatic --noinput
	docker exec shopping-django-app rm -rf manage.py
	docker cp shopping-django-app:/app/static/ ./static/
	docker cp ./static/ shopping-app:/var/www/html/static/
	rm -rf ./static/
	docker restart shopping-app

dev:
	python manage.py runserver 0.0.0.0:7001

clean:
	@rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \
	**/migrations/0*.py \
	.coverage \
	.pytest_cache \
	build/ \
	dist/ \
	*.egg-info \
	shoppingapp/db.sqlite3 \
	coverage.xml \
	htmlcov

build: clean
	python -m build .

format:
	black .
	isort . --profile black

lint: clean
	black --check .
	isort . --check-only --profile black
	flake8 . --max-line-length=100
	pydocstyle .
	mypy . --strict

migrations:
	python manage.py makemigrations
	python manage.py migrate

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

test: migrations
	pytest --ignore=tests/
	coverage xml
	coverage html

