.PHONY: static clean format lint test coverage unit-test api-test e2e-test requirements

static:
	@export SHOPPING_DEV=1 && \
	rm -rf static/ && \
	python manage.py collectstatic --no-input
	@npx @tailwindcss/cli -i ./styles/tailwind.css -o ./static/tailwind.css

static-watch:
	@export SHOPPING_DEV=1 && \
	rm -rf static/ && \
	python manage.py collectstatic --no-input
	@npx @tailwindcss/cli -i ./styles/tailwind.css -o ./static/tailwind.css --watch

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
	@pytest . --cov=. --no-cov-on-fail --cov-report term-missing
	@coverage xml
	@coverage html

coverage:
	@python -m http.server --directory htmlcov

requirements:
	uv pip compile --no-annotate requirements.in -o requirements.txt
	uv pip compile --no-annotate requirements.dev.in -o requirements.dev.txt
