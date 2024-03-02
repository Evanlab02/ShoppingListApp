.PHONY: run format lint test clean

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
	@pytest --ignore=tests/ -n auto
	@coverage xml
	@coverage html

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
	htmlcov
