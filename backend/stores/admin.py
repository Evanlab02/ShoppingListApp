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
    list_filter = ["store_type", "user", "created_at", "updated_at"]
    actions = ["make_online", "make_in_store", "make_online_and_in_store"]

    @admin.action(description="Mark selected stores as online.")
    def make_online(self, request, queryset) -> None:  # type: ignore
        """Update all selected stores to be online."""
        queryset.update(store_type=1)

    @admin.action(description="Mark selected stores as in-store.")
    def make_in_store(self, request, queryset) -> None:  # type: ignore
        """Update all selected stores to be in-store."""
        queryset.update(store_type=2)

    @admin.action(description="Mark selected stores as online and in-store.")
    def make_online_and_in_store(self, request, queryset) -> None:  # type: ignore
        """Update all selected stores as online and in-store."""
        queryset.update(store_type=3)


admin.site.register(Store, StoreAdmin)

log.info("Loaded stores admin config.")
