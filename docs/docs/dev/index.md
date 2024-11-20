# Getting Started (Development)

ShoppingListApp can currently only be worked on using docker and docker compose. This is the official way of developing, running and testing it locally.

## Pre-requisites

Before you dive in, make sure you have the following installed on your machine:

- Docker
- Docker Compose
- Git

### Step 1: Create a .env.dev File

Set up a `.env.dev` file in the root of your project that looks similar to this:

```.env
# POSTGRES CONFIG
POSTGRES_PASSWORD=<PASSWORD_OF_YOUR_CHOOSING>
POSTGRES_DB=shopping-db

# PGADMIN CONFIG
PGADMIN_DEFAULT_EMAIL=<EMAIL_OF_YOUR_CHOOSING>
PGADMIN_DEFAULT_PASSWORD=<PASSWORD_OF_YOUR_CHOOSING>

# SHOPPING APP CONFIG
SHOPPING_DJANGO_KEY=<SOMETHING_LONGER_THAN_50_CHARACTERS_CONTAINING_SPECIAL_CHARACTERS>
SHOPPING_DJANGO_HOST=localhost
SHOPPING_DATABASE_NAME=shopping-db
SHOPPING_DATABASE_USER=postgres
SHOPPING_DATABASE_PASSWORD=<PASSWORD_USED_ABOVE_FOR_POSTGRES_PASSWORD>
SHOPPING_DB_HOST=shopping-db
SHOPPING_DB_PORT=5432
SHOPPING_DEFAULT_SETTINGS_MODULE=shoppingapp.settings.settings
```

You only need to adjust the following values:

- `POSTGRES_PASSWORD`
- `PGADMIN_DEFAULT_EMAIL`
- `PGADMIN_DEFAULT_PASSWORD`
- `SHOPPING_DJANGO_KEY`
- `SHOPPING_DATABASE_PASSWORD`
- `SHOPPING_DJANGO_HOST`

### Step 2: Run Using Docker

Once you’ve set up your `.env.dev` variables, you can run the compose stack using Docker:

```bash
docker compose -f compose.dev.yaml watch
# OR
make dev
```

### Step 3: Create Your Superuser

To access all the cool features, you need to create a superuser. Run the following command:

```bash
docker exec -it shopping-django-admin python manage.py createsuperuser
```
