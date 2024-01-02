"""Contains the URL patterns for the stores app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="store_create_page"),
    path(views.CREATE_ACTION, views.create_page_action, name="store_create_action"),
    path(views.DETAIL_PAGE, views.detail_page, name="store_detail_page"),
]
