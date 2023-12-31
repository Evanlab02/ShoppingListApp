include .env

BE_DJ_KEY := $(shell cat secrets/djkey.txt)

.PHONY : all clean static sync up down maintenance maintenance-down

clean:
	rm -rf static

up: secrets/djkey.txt .env clean
	docker compose up -d
	docker run --name setup --env DJANGO_KEY=$(BE_DJ_KEY) -it ghcr.io/evanlab02/shoppingappbe:latest python manage.py collectstatic --noinput
	docker cp setup:/app/static/ ./static/
	docker rm setup
	docker cp ./static/ shoppinglistapp-shopping-django-site-1:/var/www/html/static/
	docker restart shoppinglistapp-shopping-django-site-1

down:
	docker compose down 

maintenance:
	docker compose -f maintenance/compose.yml up -d

maintenance-down:
	docker compose -f maintenance/compose.yml down

static: clean
	docker run --name setup --env DJANGO_KEY=$(BE_DJ_KEY) -it ghcr.io/evanlab02/shoppingappbe:latest python manage.py collectstatic --noinput
	docker cp setup:/app/static/ ./static/
	docker rm setup
	@echo "Please copy over static files to the site container"
