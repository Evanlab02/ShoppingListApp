"""Contains the admin configuration for the stores app."""

import logging

from django.contrib import admin
from django.contrib.admin import ModelAdmin

from items.models import ShoppingItem

log = logging.getLogger(__name__)


class ShoppingItemAdmin(ModelAdmin):  # type: ignore
    """Admin configuration for the shopping item model."""

    list_display = [
        "name",
        "price",
        "store",
        "user",
        "created_at",
        "updated_at",
    ]
    list_filter = ["store", "user", "created_at", "updated_at"]
    search_fields = ["name", "description"]


admin.site.register(ShoppingItem, ShoppingItemAdmin)
