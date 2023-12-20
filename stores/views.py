"""Contains the views for the stores app."""

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

CREATE_PAGE = "create"


@require_http_methods(["GET"])
@login_required(login_url="/")
def create_page(request: HttpRequest) -> HttpResponse:
    """
    Render the create page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    error = request.GET.get("error")
    context = {"error": error}
    return render(request, "stores/create.html", context)
