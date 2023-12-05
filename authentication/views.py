"""Contains views for the authentication app."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.errors.api_exceptions import UserAlreadyLoggedIn
from authentication.services.views.user_service import get_login_view_context


@require_http_methods(["GET"])
def login_view(request: HttpRequest) -> HttpResponse:
    """
    Handle the login view.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        context = get_login_view_context(request)
        return render(request, "auth/index.html", context.model_dump())
    except UserAlreadyLoggedIn:
        return HttpResponseRedirect("/shopping/dashboard/")
