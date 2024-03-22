"""Contains the admin configuration for the stores app."""

from django.contrib import admin

from items.models import ShoppingItem

admin.site.register(ShoppingItem)
