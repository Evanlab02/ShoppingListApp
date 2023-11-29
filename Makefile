.PHONY: clean requirements format lint up down dev migrations

clean:
	rm -rf .mypy_cache \
	**/__pycache__ \
	**/**/__pycache__ \

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt

format:
	black .
	isort . --profile black

lint:
	black --check .
	isort . --check-only --profile black
	flake8 . --max-line-length=100
	mypy .
	pydocstyle .

up:
	docker compose up -d

down:
	docker compose down

dev:
	python manage.py runserver 0.0.0.0:7001

migrations:
	python manage.py makemigrations
	python manage.py migrate
