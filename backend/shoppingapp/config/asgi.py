"""
ASGI config for shoppingapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import logging
import os

from django.core.asgi import get_asgi_application

log = logging.getLogger(__name__)

SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shoppingapp.core.settings")
app = get_asgi_application()
