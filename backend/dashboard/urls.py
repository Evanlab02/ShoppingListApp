"""Contains the urls for the dashboard app."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("debug/<int:status_code>", views.debug_status_code, name="debug_status_code"),
]
