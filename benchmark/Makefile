.PHONY: format
format:
	@black .
	@isort . --profile black

.PHONY: lint
lint:
	@black --check src/
	@isort src/ --check-only --profile black
	@flake8 src/ --max-line-length=100
	@mypy src/ --strict
