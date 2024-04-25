"""Contains the URL patterns for the items app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="item_create_page"),
    path(views.CREATE_ACTION, views.create_action, name="item_create_action"),
    path(views.OVERVIEW_PAGE, views.get_overview_page, name="item_overview_page"),
    path(
        views.PERSONALIZED_OVERVIEW_PAGE,
        views.get_personalized_overview_page,
        name="item_personalized_overview_page",
    ),
]
