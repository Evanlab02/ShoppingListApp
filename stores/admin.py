"""Contains the admin configuration for the stores app."""

from django.contrib import admin

from stores.models import ShoppingStore as Store

admin.site.register(Store)
