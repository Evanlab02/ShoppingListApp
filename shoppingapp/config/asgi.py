"""
ASGI config for shoppingapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

import uvicorn
from django.core.asgi import get_asgi_application


def main() -> None:
    """Contains the main entrypoint for the ASGI server."""
    DEFAULT_SETTINGS = "shoppingapp.settings.settings"
    SETTINGS_MODULE = os.getenv("DEFAULT_SETTINGS_MODULE", DEFAULT_SETTINGS)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_MODULE)
    application = get_asgi_application()
    uvicorn.run(application, host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
