"""Contains the admin configuration for the stores app."""

import logging

from django.contrib import admin

from items.models import ShoppingItem

log = logging.getLogger(__name__)
log.info("Items app admin loading...")

admin.site.register(ShoppingItem)

log.info("Items app admin loaded.")
