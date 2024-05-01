.PHONY: static clean format lint test coverage

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
	@pytest . -n auto
	@coverage xml
	@coverage html

coverage:
	@python -m http.server --directory htmlcov