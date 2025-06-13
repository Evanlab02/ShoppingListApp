"""Contains the views for the dashboard app."""

import logging

from django.core.exceptions import BadRequest, ImproperlyConfigured, PermissionDenied
from django.http import Http404, HttpRequest, HttpResponse
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


@require_http_methods(["GET"])
def debug_status_code(request: HttpRequest, status_code: int) -> HttpResponse:
    """
    Debug a status code.

    Args:
        request (HttpRequest): The request object.
        status_code (int): The status code to debug.

    Returns:
        HttpResponse: The response object.

    Raises:
        Http404: If status_code is 404.
        PermissionDenied: If status_code is 403.
        SuspiciousOperation: If status_code is 400.
        Exception: If status_code is 500.
    """
    if status_code == 404:
        raise Http404("Debug 404 error")
    elif status_code == 403:
        raise PermissionDenied("Debug 403 error")
    elif status_code == 400:
        raise BadRequest("Debug 400 error")
    elif status_code == 500:
        raise ImproperlyConfigured("Debug 500 error")
    else:
        return HttpResponse(f"Debug status code: {status_code}", status=status_code)


def bad_request_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """
    Handle 400 Bad Request errors.

    Args:
        request (HttpRequest): The request object.
        exception (Exception | None): The exception object.

    Returns:
        HttpResponse: The response object.
    """
    LOG.error(f"400 Bad Request: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/400.html", context, status=400)


def permission_denied_view(
    request: HttpRequest, exception: Exception | None = None
) -> HttpResponse:
    """
    Handle 403 Forbidden errors.

    Args:
        request (HttpRequest): The request object.
        exception (Exception | None): The exception object.

    Returns:
        HttpResponse: The response object.
    """
    LOG.error(f"403 Forbidden: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/403.html", context, status=403)


def not_found_view(request: HttpRequest, exception: Exception | None = None) -> HttpResponse:
    """
    Handle 404 Not Found errors.

    Args:
        request (HttpRequest): The request object.
        exception (Exception | None): The exception object.

    Returns:
        HttpResponse: The response object.
    """
    LOG.error(f"404 Not Found: {exception}")
    context = {"exception": GENERIC_ERROR_MESSAGE}
    return render(request, "dashboard/err/404.html", context, status=404)


def server_error_view(request: HttpRequest) -> HttpResponse:
    """
    Handle 500 Internal Server errors.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    return render(request, "dashboard/err/500.html", status=500)
