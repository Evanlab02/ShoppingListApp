"""Contains the urls for the authentication app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.login_view, name="login_page"),
]
