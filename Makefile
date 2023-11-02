BE_NAME = shopping-django-app
BE_VERSION := $(shell cat backend/version.txt)
BE_DJ_KEY := $(shell cat secrets/djkey.txt)
SERVER_NAME = shopping-django-site
SERVER_VERSION := $(shell cat version.txt)

.PHONY : build-backend build-server build up down uninstall maintenance maintenance-down

build-backend:
	@echo "----- BACKEND -----"
	@echo "Removing old static files"
	@rm -rf static
	@echo "Building Backend"
	@docker build -t $(BE_NAME):$(BE_VERSION) ./backend
	@echo "Creating Static Files"
	@docker run --name setup --env DJANGO_KEY=$(BE_DJ_KEY) -it ${BE_NAME}:${BE_VERSION} python manage.py collectstatic --noinput
	@ echo "Copying Static Files"
	@docker cp setup:/app/static/ ./static/
	@echo "Cleaning up"
	@docker rm setup
	@echo ""

build-server:
	@echo "----- SERVER -----"
	@docker build -t $(SERVER_NAME):$(SERVER_VERSION) .
	@echo ""

build: build-backend build-server
	@echo "----- MAINTENANCE -----"
	docker build -t maintenance:1.0.0 ./maintenance
	@echo "Created Images"

up:
	docker compose up -d

down: 
	docker compose down

uninstall: clean
	docker compose down -v --rmi all --remove-orphans

maintenance:
	docker compose -f maintenance/compose.yml up -d

maintenance-down:
	docker compose -f maintenance/compose.yml down