"""Contains admin configuration for the authentication app."""

import logging

from django.contrib import admin

from authentication.models import ApiClient

log = logging.getLogger(__name__)
log.info("Authentication admin config loading...")


class ApiClientAdmin(admin.ModelAdmin):  # type: ignore
    """Admin configuration for the shoppingstore app."""

    list_display = ("name", "user", "is_active")
    list_display_links = ("name",)
    search_fields = ("name",)
    list_filter = ("is_active",)
    list_per_page = 10


admin.site.register(ApiClient, ApiClientAdmin)

log.info("Authentication admin config loaded.")
