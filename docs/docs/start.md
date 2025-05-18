# Getting Started

Welcome to the **ShoppingListApp**! 🎉 Please note that this app is integrated into another project of mine called [HomePortal](https://github.com/Evanlab02/HomePortal). You can use ShoppingListApp within that project, but it’s perfectly fine to set it up on its own as well. Let’s get started!

!!! warning "Warning"
    The documentation is currently under a major rework following a refactor of the project. Please note that is in preparation for V0.18 which is setting the foundations for the project going further and should be significantly more stable and **if** all goes well, maintain backwards compatibility much better than previous versions. The goal is in subsequent releases to have a foundation that guarantees backwards compatibility up until the V1 release and beyond.

## Pre-requisites

Before you dive in, make sure you have the following installed on your machine:

- Docker
- Docker Compose
- Git

## Method 1: Using Git

Clone the repository onto your machine with the following command:

```bash
git clone git@github.com:Evanlab02/ShoppingListApp.git
```

### Step 1: Create a .env File

Set up a `.env` file in the root of your project that looks similar to this:

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

Once you’ve set up your `.env` variables, you can run the app using Docker:

```bash
docker compose pull
docker compose up -d
```

### Step 3: Create Your Superuser

To access all the cool features, you need to create a superuser. Run the following command:

```bash
docker exec -it shopping-django-admin python manage.py createsuperuser
```

### Step 4: Login and Use the Shopping List App

Congratulations! You should now be able to log in and access the Shopping List App on your host. Happy shopping! 🛒

## Method 2: Using Pre-packaged Zip

COMING SOON!
