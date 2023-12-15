"""Contains admin configuration for the authentication app."""

from django.contrib import admin

from authentication.models import ApiClient

admin.site.register(ApiClient)
