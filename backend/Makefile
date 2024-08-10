.PHONY: static clean format lint test coverage unit-test api-test e2e-test requirements

static:
	@rm -rf static/
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

format:
	@black .
	@isort . --profile black

lint:
	@black --check .
	@isort . --check-only --profile black
	@flake8 . --max-line-length=100
	@mypy . --strict

test:
	@pytest . -n auto --cov=. --no-cov-on-fail --cov-report term-missing
	@coverage xml
	@coverage html

coverage:
	@python -m http.server --directory htmlcov

unit-test:
	@pytest . -vv --cov=. --no-cov-on-fail --cov-report term-missing \
	--ignore=authentication/tests/api/ \
	--ignore=authentication/tests/E2E/ \
	--ignore=items/tests/api/ \
	--ignore=items/tests/E2E/ \
	--ignore=stores/tests/api/ \
	--ignore=stores/tests/E2E/ \

api-test:
	@pytest **/tests/api/ -vv

e2e-test:
	@pytest **/tests/E2E/ -n auto

requirements:
	pipenv requirements > requirements.txt
	pipenv requirements --dev > requirements-dev.txt