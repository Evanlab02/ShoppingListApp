# ShoppingListApp - Configuration

The application is configured through a set of environment variables. The table below lists every variable, whether it is required, the default that will be assumed when it is omitted, and its purpose.

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `SHOPPING_DJANGO_KEY` | Yes | – | Secret key used by Django for cryptographic signing. Must be unique and kept secret in production. |
| `SHOPPING_DJANGO_HOST` | Yes | – | External hostname of the application that will be added to Django's `ALLOWED_HOSTS`. |
| `SHOPPING_DATABASE_NAME` | Yes | – | PostgreSQL database name used by the application. |
| `SHOPPING_DATABASE_USER` | Yes | – | PostgreSQL user that owns `SHOPPING_DATABASE_NAME`. |
| `SHOPPING_DATABASE_PASSWORD` | Yes | – | Password for `SHOPPING_DATABASE_USER`. |
| `SHOPPING_DB_HOST` | Yes | – | Hostname of the PostgreSQL server (e.g. `shopping-db` when using Docker Compose). |
| `SHOPPING_DB_PORT` | No | `5432` | Port on which PostgreSQL is listening. |
| `SHOPPING_REDIS_HOST` | Yes | – | Hostname of the Redis instance used for the default Django cache backend. |
| `SHOPPING_DEV` | No | `0` | When set to `1`, the app runs in development mode (`DEBUG = True`) and enables extra tooling such as `django-silk`. |
| `DJANGO_SETTINGS_MODULE` | No | Varies – see below | Import path to the Django settings module. Each entry-point provides a sensible default; override when you want to pick a different settings module. |
| `SHOPPING_ALLOW_LEGACY_HASHING` | No | `1` | When `1`, legacy PBKDF2 hashers are **allowed** in addition to Argon2. Set to `0` to disable them. You need to ensure all users have migrated to Argon2 otherwise this will lock users out. |
| `SHOPPING_FORCE_LEGACY_HASHING` | No | `0` | When `1`, **forces** the use of legacy PBKDF2 hashers only, overriding `SHOPPING_ALLOW_LEGACY_HASHING`. This forces the application not to use Argon2 hashing, this is only to be used temporarily if the Argon2 hashing is causing major failures and is a fix until the Argon2 hashing is stable. Please do not use if not necessary. |

### Defaults for `DJANGO_SETTINGS_MODULE`
Depending on how the application is started, a default is supplied automatically:

* `manage.py` (CLI commands) – `shoppingapp.dev.settings`
* `shoppingapp/config/asgi.py` – `shoppingapp.core.settings`
* `shoppingapp/config/wsgi.py` – `shoppingapp.settings.settings` (This needs to be adjusted as this is outdated. This will be fixed once we have a synchronous implementation for the application.)

You rarely need to set `DJANGO_SETTINGS_MODULE` yourself unless you want to point to a custom settings module.
