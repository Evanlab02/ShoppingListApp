"""Contains the views for the stores app."""

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from pydantic import ValidationError

from authentication.decorators import async_login_required
from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.schemas.contexts import BaseContext, StoreDetailContext
from stores.schemas.input import NewStore
from stores.services import store_service

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"
DETAIL_PAGE = "detail/<int:store_id>"


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
    context = BaseContext(
        page_title="Create Store",
        error=error,
    )
    return render(request, "stores/create.html", context.model_dump())


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
        store = await store_service.create(new_store, user)
        store_id = store.id  # type: ignore
        return HttpResponseRedirect(f"/stores/detail/{store_id}")
    except (StoreAlreadyExists, InvalidStoreType) as error:
        return HttpResponseRedirect(f"/stores/{CREATE_PAGE}?error={str(error)}")


@require_http_methods(["GET"])
@async_login_required
async def detail_page(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Render the detail page.

    The detail page is used to display detailed information about a store. Some of the information
    on this page includes the name, description, type, the time the store was created,
    who created the store, the number of related items and a table containing all the related
    items.

    Args:
        request (HttpRequest): The request object.
        store_id (int): The store id.

    Returns:
        HttpResponse: The response object.
    """
    try:
        store = await store_service.get_store_detail(store_id)
        context = StoreDetailContext(
            store=store,
            page_title=f"Store - {store.name}",  # type: ignore
            is_personal=False,
            show_advanced_navigation=True,
        )
        return render(request, "stores/detail.html", context.model_dump())
    except StoreDoesNotExist:
        return HttpResponse("This store does not exist.")
