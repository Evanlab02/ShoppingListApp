"""Contains admin configuration for the authentication app."""

import logging

from django.contrib import admin

from authentication.models import ApiClient

log = logging.getLogger(__name__)


class ApiClientAdmin(admin.ModelAdmin):  # type: ignore
    """Admin configuration for the shoppingstore app."""

    list_display = ("user", "is_active")
    list_display_links = ("user",)
    search_fields = ("user",)
    list_filter = ("is_active",)
    list_per_page = 10


admin.site.register(ApiClient, ApiClientAdmin)
