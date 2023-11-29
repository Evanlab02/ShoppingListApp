.PHONY: clean requirements format lint

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
