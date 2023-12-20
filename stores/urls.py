"""Contains the URL patterns for the stores app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="store_create_page"),
]
