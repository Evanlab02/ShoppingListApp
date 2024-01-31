"""Contains the URL patterns for the stores app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="store_create_page"),
    path(views.CREATE_ACTION, views.create_page_action, name="store_create_action"),
    path(views.DETAIL_PAGE, views.detail_page, name="store_detail_page"),
    path(views.OVERVIEW_PAGE, views.overview_page, name="store_overview_page"),
    path(views.UPDATE_PAGE, views.update_page, name="store_update_page"),
    path(
        views.PERSONAL_OVERVIEW_PAGE,
        views.personal_overview_page,
        name="store_personal_overview_page",
    ),
]
