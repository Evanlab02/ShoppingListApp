"""Contains the views for the items app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from authentication.decorators.login import async_login_required
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.schemas.contexts import (
    ItemCreateContext,
    ItemDetailContext,
    ItemOverviewContext,
    ItemUpdateContext,
)
from items.schemas.output import ItemSchema
from items.services.item_service import ItemService
from shoppingapp.utilities.utils import get_overview_params
from stores.services.store_service import StoreService

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"
OVERVIEW_PAGE = ""
PERSONALIZED_OVERVIEW_PAGE = "me"
DETAIL_PAGE = "detail/<int:item_id>"
UPDATE_PAGE = "update/<int:item_id>"
UPDATE_ACTION = "update/action"
DELETE_PAGE = "delete/<int:item_id>"
DELETE_ACTION = "delete/action"

log = logging.getLogger(__name__)

SERVICE = ItemService()
STORE_SERVICE = StoreService()


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
    user = await request.auser()
    error = request.GET.get("error")

    if error:
        logging.warning(f"{user.id} encountered error: {error}")

    stores = await STORE_SERVICE.get_stores(limit=1000)
    context = ItemCreateContext(page_title="Create Item", error=error, stores=stores.stores)
    return render(request, "items/create.html", context.model_dump())


@require_http_methods(["POST"])
@async_login_required
async def create_action(request: HttpRequest) -> HttpResponse:
    """
    Create an item.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = await request.auser()

    item_name = request.POST.get("item-input")
    store_input = request.POST.get("store-input")
    price_input = request.POST.get("price-input")
    description_input = request.POST.get("description-input", "")

    if not store_input or not price_input or not item_name:
        return HttpResponseRedirect(f"{reverse('item_create_page')}?error=Missing required fields.")

    try:
        store_id = int(store_input)
        price = float(price_input)
        item = await SERVICE.create_item(
            user=user,
            store_id=store_id,
            description=description_input,
            price=price,
            name=item_name,
        )
        item_id = item.id
        redirect_url = f"{reverse('item_detail_page', kwargs={'item_id': item_id})}"
        return HttpResponseRedirect(redirect_url)
    except ValueError as err:
        logging.warning(err)
        return HttpResponseRedirect(f"{reverse('item_create_page')}?error=Invalid input.")
    except ItemAlreadyExists as err:
        logging.warning(err)
        return HttpResponseRedirect(f"{reverse('item_create_page')}?error=Item Already Exists.")


async def _get_overview_context(
    request: HttpRequest, params: dict[str, int], is_personalized: bool = False
) -> ItemOverviewContext:
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
        (await request.auser(), "Your Items") if is_personalized else (None, "All Items")
    )

    pagination = await SERVICE.get_items(page=page, items_per_page=limit, user=user)
    aggregation = await SERVICE.aggregate(user=user)
    return ItemOverviewContext(
        pagination=pagination,
        aggregation=aggregation,
        page_title=page_title,
        is_overview=True,
        is_personal=is_personalized,
        show_advanced_navigation=True,
    )


@require_http_methods(["GET"])
@async_login_required
async def get_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the overview page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    params = get_overview_params(request)
    context = await _get_overview_context(request=request, params=params)
    return render(request, "items/overview.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def get_personalized_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the personalized overview page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    params = get_overview_params(request)
    context = await _get_overview_context(request=request, params=params, is_personalized=True)
    return render(request, "items/overview.html", context.model_dump())


@require_http_methods(["GET"])
@async_login_required
async def get_item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Render the item detail page.

    Args:
        request(HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    try:
        item = await SERVICE.get_item_detail(item_id=item_id)
        context = ItemDetailContext(
            item=ItemSchema.from_orm(item),
            page_title=f"Item - {item.name}",
            is_personal=False,
            show_advanced_navigation=True,
        )
        return render(request, "items/detail.html", context.model_dump())
    except ItemDoesNotExist:
        return HttpResponse(f"Item with id '{item_id}' does not exist.", status=404)


@require_http_methods(["GET"])
@async_login_required
async def update_page(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Render the update page.

    Args:
        request (HttpRequest): The request object.
        item_id (int): The item id.

    Returns:
        HttpResponse: The response object.
    """
    try:
        item = await SERVICE.get_item_detail(item_id=item_id)
        stores = await STORE_SERVICE.get_stores(limit=1000)
        context = ItemUpdateContext(
            page_title="Update Item",
            item=ItemSchema.from_orm(item),
            stores=stores.stores,
            error=request.GET.get("error"),
        )
        return render(request, "items/update.html", context.model_dump())
    except ItemDoesNotExist:
        return HttpResponse(f"Item with id '{item_id}' does not exist.", status=404)


@require_http_methods(["POST"])
@async_login_required
async def update_action(request: HttpRequest) -> HttpResponse:
    """
    Update an item with the given id.

    Args:
        request (HttpRequest): The request.

    Returns:
        HttpResponse: The response from the API.
    """
    user = await request.auser()
    item_id = request.POST.get("item-id")
    item_name = request.POST.get("item-input")
    store_id = request.POST.get("store-input")
    price = request.POST.get("price-input")
    description = request.POST.get("description-input")

    try:
        formatted_item_id = int(item_id) if item_id else None
        formatted_store_id = int(store_id) if store_id else None
        formatted_price = float(price) if price else None
    except ValueError:
        error = "Could not format input for item update, please try again."
        return HttpResponse(error, status=400)

    if not item_id or not formatted_item_id:
        error = "Could not find ID for update, please try again."
        return HttpResponse(error, status=400)

    try:
        item = await SERVICE.update_item(
            user=user,
            item_id=formatted_item_id,
            new_name=item_name,
            new_store_id=formatted_store_id,
            new_price=formatted_price,
            new_description=description,
        )
        redirect_url = f"{reverse('item_detail_page', kwargs={'item_id': item.id})}"
        return HttpResponseRedirect(redirect_url)
    except ItemDoesNotExist:
        error = f"Could not find item with ID: {formatted_item_id}."
        return HttpResponse(error, status=400)
    except ItemAlreadyExists:
        error = "Item already exists in that store."
        return HttpResponseRedirect(
            f"{reverse('item_update_page', kwargs={'item_id': item_id})}?error={error}"
        )


@require_http_methods(["GET"])
@async_login_required
async def delete_page(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Render the delete page.

    Args:
        request (HttpRequest): The request object.
        item_id (int): The item id.

    Returns:
        HttpResponse: The response object.
    """
    user = await request.auser()
    error = request.GET.get("error")

    try:
        item = await SERVICE.get_item_for_user(item_id=item_id, user=user)
        context = ItemDetailContext(
            error=error,
            page_title="Delete Item",
            item=ItemSchema.from_orm(item),
        )
        return render(request, "items/delete.html", context.model_dump())
    except ItemDoesNotExist:
        logging.error("Could not find item for deletion.")
        return HttpResponse("Item does not exist.", status=404)


@require_http_methods(["POST"])
@async_login_required
async def delete_action(request: HttpRequest) -> HttpResponse:
    """
    Delete an item with the given id.

    Args:
        request (HttpRequest): The request.

    Returns:
        HttpResponse: The response from the API.
    """
    user = await request.auser()
    item_id = request.POST.get("item-id")

    try:
        formatted_item_id = int(item_id) if item_id else None
    except ValueError:
        logging.error("Retrieved input that could not be formatted for item deletion.")
        return HttpResponse(
            "Could not format input for item deletion, please try again.", status=400
        )

    if not item_id or not formatted_item_id:
        logging.error("Item ID is required for deletion of an item.")
        return HttpResponse("Could not find ID for deletion, please try again.", status=400)

    try:
        await SERVICE.delete_item(user=user, item_id=formatted_item_id)
        return HttpResponseRedirect(f"{reverse('item_personalized_overview_page')}")
    except ItemDoesNotExist:
        logging.error("Item does not exist for deletion.")
        return HttpResponse(f"Could not find item with ID: {formatted_item_id}.", status=404)
