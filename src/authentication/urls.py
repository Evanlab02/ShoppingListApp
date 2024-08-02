"""Contains the urls for the authentication app."""

import logging

from django.urls import path

from . import views

log = logging.getLogger(__name__)
log.info("Auth URLs loading...")

urlpatterns = [
    path(views.LOGIN_ROUTE, views.login_view, name="login_page"),
    path(views.LOGIN_ACTION_ROUTE, views.login_action, name="login_action"),
    path(views.REGISTER_ROUTE, views.register_view, name="register_page"),
    path(views.REGISTER_ACTION_ROUTE, views.register_action, name="register_action"),
    path(views.LOGOUT_ROUTE, views.logout_view, name="logout_page"),
    path(views.LOGOUT_ACTION_ROUTE, views.logout_action, name="logout_action"),
    path(views.CONFIRM_TOKEN_ROUTE, views.confirm_token, name="confirm_token"),
    path(views.ENABLE_CLIENT_ROUTE, views.enable_api_client, name="enable_client"),
    path(views.DISABLE_CLIENT_ROUTE, views.disable_api_client, name="disable_client"),
]

log.info("Auth URLs loaded.")
