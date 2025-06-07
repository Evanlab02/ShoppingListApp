"""Contains the views for the dashboard app."""

import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators import login_required

GENERIC_ERROR_MESSAGE = "No Information Provided"
LOG = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET"])
def dashboard_view(request: HttpRequest) -> HttpResponse:
    """Render the dashboard page."""
    return render(request, "dashboard/index.html")


def bad_request_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Handle 400 Bad Request errors."""
    LOG.error(f"400 Bad Request: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/400.html", context, status=400)


def permission_denied_view(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    """Handle 403 Forbidden errors."""
    LOG.error(f"403 Forbidden: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/403.html", context, status=403)


def not_found_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """Handle 404 Not Found errors."""
    LOG.error(f"404 Not Found: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/404.html", context, status=404)


def server_error_view(request: HttpRequest) -> HttpResponse:
    """Handle 500 Internal Server errors."""
    return render(request, "dashboard/err/500.html", status=500)
