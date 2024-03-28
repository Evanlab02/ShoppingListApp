# Installation Guide

Find below the installation guide for the Shopping List App.

## Prerequisites

You need to have the following installed to run and setup the Shopping List App:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Make](https://www.gnu.org/software/make/)
- [Ubuntu or ubuntu based distro](https://ubuntu.com/download)

## Download a release

You can download a release from the releases page [here](https://github.com/Evanlab02/ShoppingListApp/releases)

## Setup

1. Extract the release zip file 
2. Please do not rename the project folder when extracting is complete as this is used to determine container names and we rely on that to be the same in the setup.
3. Open a terminal in the extracted folder
4. Run the following command to setup the app:

```bash
./setup.sh
```

5. Follow the instructions in the terminal

### Changing values

All the values you specified as part of the setup can be changed in the `.env` file in the root of the project.

You can also change the secrets by changing the .txt files in the secrets folder.

!IMPORTANT!: Please change the backend version to 0.12.3 in the .env file, this is due to a bug in the latest version of the backend.

## Running the app

To run the app, run the following command(s):

```bash
make up

# or

docker compose up -d
docker run --name setup --env DJANGO_KEY=$(BE_DJ_KEY) -it ghcr.io/evanlab02/shoppingappbe:latest python manage.py collectstatic --noinput
docker cp setup:/app/static/ ./static/
docker rm setup
docker cp ./static/ shoppinglistapp-shopping-django-site-1:/var/www/html/static/
```

## Migrations and super user

You need to db migrations and create a super user to use the app. Migrations only have to be done once on setup and when the app gets updated.

You will also need to redo these steps if you delete the volume that contains the database data. The volume is how we store the data between container restarts.

To run the migrations and create a super user, run the following commands in the shopping-django-app container, I highly recommend using docker desktop as this makes it easier to run these commands in the container:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

If you want to do it without docker desktop and you are using the CLI, you can try the following:

```bash
docker exec -it shoppinglistapp-shopping-django-app-1 bash
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

## Stopping the app

To stop the app, run the following command(s):

```bash
make down
```

Want to start it up again, you do not have to redo all the steps above, all that is required is to run the following command:

```bash
make up
```

