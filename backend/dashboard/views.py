"""Contains the views for the dashboard app."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators import login_required


@login_required
@require_http_methods(["GET"])
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Render the dashboard page."""
    return render(request, "dashboard/index.html")
