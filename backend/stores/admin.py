"""Contains the admin configuration for the stores app."""

import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from stores.models import ShoppingStore as Store

log = logging.getLogger(__name__)
log.info("Loading stores admin config...")


class StoreAdmin(ModelAdmin):  # type: ignore
    """Admin configuration class for store models."""

    list_display = ["name", "store_type", "description", "created_at", "updated_at", "user"]


admin.site.register(Store, StoreAdmin)

log.info("Loaded stores admin config.")
