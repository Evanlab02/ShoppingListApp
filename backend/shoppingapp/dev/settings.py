"""Contains the admin settings for the shopping app."""

from shoppingapp.core.settings import *  # noqa: F403 F401

DEBUG = True

ALLOWED_HOSTS = ["localhost"]

SECRET_KEY = "TEST_KEY"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # type: ignore # noqa: F405
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
