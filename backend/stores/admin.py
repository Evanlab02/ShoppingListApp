"""Contains the admin configuration for the stores app."""

import logging

from django.contrib import admin

from stores.models import ShoppingStore as Store

log = logging.getLogger(__name__)
log.info("Loading stores admin config...")

admin.site.register(Store)

log.info("Loaded stores admin config.")
