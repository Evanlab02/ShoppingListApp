"""Contains the urls for the authentication app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("login/action", views.login_action, name="login_action"),
    path("logout", views.logout_page, name="logout_page"),
    path("logout/action", views.logout_action, name="logout_action"),
    path("register", views.register_page, name="register_page"),
    path("register/action", views.register_action, name="register_action"),
]
