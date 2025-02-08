.PHONY: install

.venv:
	uv venv

requirements.txt:
	uv pip compile --no-annotate requirements.in -o requirements.txt

install: requirements.txt
	uv pip install -r requirements.txt

requirements.dev.txt:
	uv pip compile --no-annotate requirements.dev.in -o requirements.dev.txt

install-dev: requirements.dev.txt
	uv pip install -r requirements.dev.txt

format:
	@black .
	@isort . --profile black

lint:
	@black --check .
	@isort . --check-only --profile black
	@flake8 __init__.py --max-line-length=100
	@mypy __init__.py --strict
