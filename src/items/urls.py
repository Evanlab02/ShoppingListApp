"""Contains the URL patterns for the items app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="item_create_page"),
    path(views.CREATE_ACTION, views.create_action, name="item_create_action"),
    path(views.OVERVIEW_PAGE, views.get_overview_page, name="item_overview_page"),
    path(views.DETAIL_PAGE, views.get_item_detail, name="item_detail_page"),
    path(
        views.PERSONALIZED_OVERVIEW_PAGE,
        views.get_personalized_overview_page,
        name="item_personalized_overview_page",
    ),
    path(views.UPDATE_PAGE, views.update_page, name="item_update_page"),
    path(views.UPDATE_ACTION, views.update_action, name="item_update_action"),
    path(views.DELETE_PAGE, views.delete_page, name="item_delete_page"),
    path(views.DELETE_ACTION, views.delete_action, name="item_delete_action"),
]
