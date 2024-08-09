"""Contains the URL patterns for the stores app."""

import logging

from django.urls import path

from . import views

log = logging.getLogger(__name__)
log.info("Stores app URLs loading...")

urlpatterns = [
    path(views.CREATE_PAGE, views.create_page, name="store_create_page"),
    path(views.CREATE_ACTION, views.create_page_action, name="store_create_action"),
    path(views.DETAIL_PAGE, views.detail_page, name="store_detail_page"),
    path(views.OVERVIEW_PAGE, views.overview_page, name="store_overview_page"),
    path(views.UPDATE_PAGE, views.update_page, name="store_update_page"),
    path(views.UPDATE_ACTION, views.update_action, name="store_update_action"),
    path(views.DELETE_PAGE, views.delete_page, name="store_delete_page"),
    path(views.DELETE_ACTION, views.delete_action, name="store_delete_action"),
    path(
        views.PERSONAL_OVERVIEW_PAGE,
        views.personal_overview_page,
        name="store_personal_overview_page",
    ),
]

log.info("Stores app URLs loaded.")
