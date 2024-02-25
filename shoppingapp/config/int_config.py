"""
ASGI config for shoppingapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application


def main() -> None:
    """Contains the main entrypoint for the ASGI server."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoppingapp.settings.int_settings")
    application = get_asgi_application()
    return application


if __name__ == "__main__":
    main()
