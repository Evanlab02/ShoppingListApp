"""Contains the views for the dashboard app."""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

from authentication.decorators import login_required

@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Renders the dashboard page."""
    return render(request, "dashboard/index.html")
