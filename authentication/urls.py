"""Contains the urls for the authentication app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.LOGIN_ROUTE, views.login_view, name="login_page"),
    path(views.LOGIN_ACTION_ROUTE, views.login_action, name="login_action"),
    path(views.REGISTER_ROUTE, views.register_view, name="register_page"),
    path(views.REGISTER_ACTION_ROUTE, views.register_action, name="register_action"),  # type: ignore # noqa E501
]
