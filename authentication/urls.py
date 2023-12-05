"""Contains the urls for the authentication app."""

from django.urls import path

from . import views

urlpatterns = [
    path(views.LOGIN_ROUTE, views.login_view, name="login_page"),
    path(views.LOGIN_ACTION_ROUTE, views.login_action, name="login_action"),
]
