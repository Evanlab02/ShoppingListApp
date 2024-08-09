.PHONY: debug dev build up down setup requirements clean

debug:
	@docker compose -f docker/docker-compose.yaml up

dev:
	@docker compose -f docker/docker-compose.yaml watch

build:
	@docker compose -f docker/docker-compose.yaml build

up:
	@docker compose -f docker/docker-compose.yaml up -d

down:
	@docker compose -f docker/docker-compose.yaml down

super-user:
	docker exec -it shopping-django-admin python manage.py createsuperuser

requirements:
	@pipenv requirements > src/requirements.txt
	@pipenv requirements --dev > src/requirements-dev.txt

clean:
	@rm -rf site/

exec:
	docker exec -it shopping-django-app bash