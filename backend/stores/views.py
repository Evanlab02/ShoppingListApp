"""Contains the views for the stores app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators import async_login_required
from shoppingapp.schemas.shared import BaseContext
from shoppingapp.utilities.utils import get_overview_params
from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.schemas.contexts import (
    StoreContext,
    StoreDetailContext,
    StoreOverviewContext,
)
from stores.schemas.input import NewStore
from stores.services import store_service

log = logging.getLogger(__name__)
log.info("Stores app views loading...")

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"
DETAIL_PAGE = "detail/<int:store_id>"
OVERVIEW_PAGE = ""
PERSONAL_OVERVIEW_PAGE = "me"
UPDATE_PAGE = "update/<int:store_id>"
UPDATE_ACTION = "update/action/<int:store_id>"
DELETE_PAGE = "delete/<int:store_id>"
DELETE_ACTION = "delete/action"


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

    if description is None:
        description = ""

    if not store_name or not store_type:
        return HttpResponseRedirect(
            f"/stores/{CREATE_PAGE}?error=Store name and type are required."
        )

    new_store = NewStore(
        name=store_name,
        description=description,
        store_type=store_type,
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
    params = await get_overview_params(request=request)
    page = params.get("page", 1)
    limit = params.get("limit", 10)

    try:
        store, items = await store_service.get_store_detail_with_items(
            store_id=store_id, page_number=page, items_per_page=limit
        )
        context = StoreDetailContext(
            store=store,
            page_title=f"Store - {store.name}",  # type: ignore
            is_personal=False,
            show_advanced_navigation=True,
            items=items,
        )
        return render(request, "stores/detail.html", context.model_dump())
    except StoreDoesNotExist:
        return HttpResponse("This store does not exist.", status=404)


async def _get_overview_context(
    request: HttpRequest, params: dict[str, int], is_personalized: bool = False
) -> StoreOverviewContext:
    """
    Get overview context using request object and params.

    Args:
        request (HttpRequest): The request object.

    Returns:
        StoreOverviewContext: The store overview context.
    """
    page = params.get("page", 1)
    limit = params.get("limit", 10)

    user, page_title = (
        (await request.auser(), "Your Stores") if is_personalized else (None, "All Stores")
    )

    pagination = await store_service.get_stores(limit=limit, page_number=page, user=user)
    aggregation = await store_service.aggregate(user=user)
    context = StoreOverviewContext(
        pagination=pagination,
        aggregation=aggregation,
        page_title=page_title,
        is_overview=True,
        is_personal=is_personalized,
        show_advanced_navigation=True,
    )
    return context


@require_http_methods(["GET"])
@async_login_required
async def overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the overview page.

    The overview page is used to display basic information about all the stores.
    There will be some information about all the stores in the info cards.
    You will be able access each stores detail page from this page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    params = await get_overview_params(request)
    context = await _get_overview_context(request, params)
    return render(request, "stores/overview.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def personal_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the personal overview page.

    The overview page is used to display basic information about your stores.
    There will be some information about all the stores in the info cards.
    You will be able to access each stores detail page from this page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    params = await get_overview_params(request)
    context = await _get_overview_context(request, params, True)
    return render(request, "stores/overview.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def update_page(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Render the update page.

    Args:
        request (HttpRequest): The http request.
        store_id (int): The store to update.

    Returns:
        HttpResponse: The response (page).
    """
    try:
        error = request.GET.get("error")
        store = await store_service.get_store_detail(store_id=store_id)
        context = StoreContext(
            error=error,
            page_title="Update Store",
            store=store,
        )
        return render(request, "stores/update.html", context.model_dump())
    except StoreDoesNotExist:
        return HttpResponse("Store does not exist.", status=404)


@require_http_methods(["POST"])
@async_login_required
async def update_action(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Update a store with the given id.

    Args:
        request (HttpRequest): The request.
        store_id (int): The store id of the store to update.

    Returns:
        HttpResponse: The response from the API.
    """
    formatted_store_type: str | int | None = None
    user = request.user
    store_name = request.POST.get("store-input")
    store_type = request.POST.get("store-type-input")
    store_description = request.POST.get("description-input")

    try:
        formatted_store_type = int(store_type) if (store_type) else None
    except ValueError:
        formatted_store_type = store_type

    try:
        await store_service.update_store(
            store_id=store_id,
            user=user,
            store_name=store_name,
            store_type=formatted_store_type,
            store_description=store_description,
        )
    except (StoreAlreadyExists, InvalidStoreType) as error:
        return HttpResponseRedirect(f"/stores/update/{store_id}?error={error}")
    except StoreDoesNotExist:
        return HttpResponse("Store does not exist or does not belong to you.", status=404)

    return HttpResponseRedirect(f"/stores/detail/{store_id}")


@require_http_methods(["GET"])
@async_login_required
async def delete_page(request: HttpRequest, store_id: int) -> HttpResponse:
    """
    Retrieve/render the delete page.

    Args:
        request(HttpRequest): The HTTP Request.
        store_id (int): The store id of the store to delete.

    Response:
        HttpResponse: The HTTP Response.
    """
    try:
        error = request.GET.get("error")
        store = await store_service.get_store_detail(store_id=store_id)
        context = StoreContext(
            error=error,
            page_title="Delete Store",
            store=store,
        )
        return render(request, "stores/delete.html", context.model_dump())
    except StoreDoesNotExist:
        return HttpResponse("Store does not exist.", status=404)


@require_http_methods(["POST"])
@async_login_required
async def delete_action(request: HttpRequest) -> HttpResponse:
    """
    Delete a store.

    Args:
        request (HttpRequest): The HTTP Request.

    Returns:
        HttpResponse: The HTTP response.
    """
    store_id = request.POST.get("store_id")
    formatted_store_id = 0

    if not store_id:
        return HttpResponse(
            "Unexpected Error: Request Failed due to store id not being provided.",
            status=500,
        )

    try:
        formatted_store_id = int(store_id)
    except ValueError:
        return HttpResponse(
            "Unexpected Error: Request Failed due to store_id being invalid.",
            status=500,
        )

    user = request.user
    await store_service.delete_store(store_id=formatted_store_id, user=user)
    return HttpResponseRedirect("/stores/me")


log.info("Stores app views loaded.")
