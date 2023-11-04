BE_DJ_KEY := $(shell cat secrets/djkey.txt)

.PHONY : all clean static sync up down maintenance maintenance-down

uninstall:
	rm -rf app
	rm -rf backend
	rm -rf dist
	rm -rf maintenance
	rm -rf static
	rm -rf Dockerfile
	rm -rf compose.yml
	rm -rf setup.sh

clean:
	rm -rf backend
	rm -rf dist
	rm -rf static

static: secrets/djkey.txt .env
	docker build -t static-collector:latest ./backend
	docker run --name setup --env DJANGO_KEY=$(BE_DJ_KEY) -it static-collector:latest python manage.py collectstatic --noinput
	docker cp setup:/app/static/ ./static/
	docker rm setup
	docker rmi static-collector:latest

sync:
	cp ./app/application.properties ./backend/

up: secrets/djkey.txt .env static/ backend/application.properties
	docker compose up -d --build

down:
	docker compose down 

maintenance:
	docker compose -f maintenance/compose.yml up -d

maintenance-down:
	docker compose -f maintenance/compose.yml down
