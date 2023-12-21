"""Contains the views for the stores app."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from authentication.decorators import async_login_required
from stores.errors.api_exceptions import InvalidStoreType, StoreAlreadyExists
from stores.schemas.input import NewStore
from stores.services.store_service import create

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"


@require_http_methods(["GET"])
@async_login_required
async def create_page(request: HttpRequest) -> HttpResponse:
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


@require_http_methods(["POST"])
@async_login_required
async def create_page_action(request: HttpRequest) -> HttpResponse:
    """
    Create page action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    store_name = request.POST.get("store-input")
    description = request.POST.get("description-input")
    store_type = request.POST.get("store-type-input")

    try:
        new_store = NewStore(
            name=store_name,
            description=description,
            store_type=store_type,
        )
    except ValidationError:
        return HttpResponseRedirect(
            f"/stores/{CREATE_PAGE}?error=Validation failed, please try again."
        )

    try:
        store = await create(new_store, user)
        store_id = store.id  # type: ignore
        return HttpResponseRedirect(f"/stores/detail/{store_id}")
    except (StoreAlreadyExists, InvalidStoreType) as error:
        return HttpResponseRedirect(f"/stores/{CREATE_PAGE}?error={str(error)}")
