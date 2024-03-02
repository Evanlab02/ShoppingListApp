.PHONY: debug build up down requirements clean

debug:
	@docker compose -f docker/docker-compose.yaml up --build

build:
	@docker compose -f docker/docker-compose.yaml build

up:
	@docker compose -f docker/docker-compose.yaml up -d

down:
	@docker compose -f docker/docker-compose.yaml down

requirements:
	@pipenv requirements > requirements.txt
	@pipenv requirements --dev > requirements-dev.txt

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
	coverage.xml \
	htmlcov \
	static
