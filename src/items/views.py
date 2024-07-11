"""Contains the views for the items app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators.login import async_login_required
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.schemas.contexts import (
    ItemCreateContext,
    ItemDetailContext,
    ItemOverviewContext,
    ItemUpdateContext,
)
from items.services import item_service
from shoppingapp.utilities.utils import get_overview_params
from stores.services import store_service

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"
OVERVIEW_PAGE = ""
PERSONALIZED_OVERVIEW_PAGE = "me"
DETAIL_PAGE = "detail/<int:item_id>"
UPDATE_PAGE = "update/<int:item_id>"
UPDATE_ACTION = "update/action"
DELETE_PAGE = "delete/<int:item_id>"
DELETE_ACTION = "delete/action"


async def _handle_validation_error(
    name: str | None, store_id: str | None, price: str | None, description: str | None
) -> HttpResponseRedirect:
    """Handle a validation error."""
    logging.error("Item creation failed: Validation Error")
    logging.error(f"ITEM: {name}")
    logging.error(f"STORE: {store_id}")
    logging.error(f"PRICE: {price}")
    logging.error(f"DESCRIPTION: {description}")
    return HttpResponseRedirect("/items/create?error=Validation failed, please try again.")


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
    logging.info(f"{request.user.id} requested item create page.")
    error = request.GET.get("error")

    if error:
        logging.warning(f"{request.user.id} encountered error: {error}")

    stores = await store_service.get_stores(limit=1000)
    context = ItemCreateContext(page_title="Create Item", error=error, stores=stores.stores)
    return render(request, "items/create.html", context.model_dump())


@require_http_methods(["POST"])
@async_login_required
async def create_action(request: HttpRequest) -> HttpResponse:
    """
    Create page action.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    user = request.user
    logging.info(f"{user.id} attempting to create an item.")

    item_name = request.POST.get("item-input")
    store_input = request.POST.get("store-input")
    price_input = request.POST.get("price-input")
    description_input = request.POST.get("description-input", "")

    if not store_input or not price_input or not item_name:
        return await _handle_validation_error(
            name=item_name,
            store_id=store_input,
            description=description_input,
            price=price_input,
        )

    try:
        store_id = int(store_input)
        price = float(price_input)
        item = await item_service.create_item(
            user=user,
            store_id=store_id,
            description=description_input,
            price=price,
            name=item_name,
        )
        item_id = item.id  # type: ignore
        redirect_url = f"/items/detail/{item_id}"
        logging.info(f"Redirecting {user.id} to {redirect_url}")
        return HttpResponseRedirect(redirect_url)
    except ValueError as err:
        logging.warning(err)
        return await _handle_validation_error(
            name=item_name,
            store_id=store_input,
            description=description_input,
            price=price_input,
        )
    except ItemAlreadyExists as err:
        logging.warning(err)
        return HttpResponseRedirect("/items/create?error=Item Already Exists.")


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

    user, page_title = (request.user, "Your Items") if is_personalized else (None, "All Items")

    pagination = await item_service.get_items(page=page, items_per_page=limit, user=user)
    aggregation = await item_service.aggregate(user=user)
    context = ItemOverviewContext(
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
async def get_overview_page(request: HttpRequest) -> HttpResponse:
    """
    Render the overview page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    params = await get_overview_params(request=request)
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
    params = await get_overview_params(request=request)
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
        item = await item_service.get_item_detail(item_id=item_id)
        context = ItemDetailContext(
            item=item,
            page_title=f"Item - {item.name}",  # type: ignore
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
    logging.info(f"Requested update item view for item: {item_id}")
    try:
        item = await item_service.get_item_detail(item_id=item_id)
        stores = await store_service.get_stores(limit=1000)
        context = ItemUpdateContext(
            page_title="Update Item",
            item=item,
            stores=stores.stores,
            error=request.GET.get("error"),
        )
        logging.info(f"Returning update view for item: {item_id}")
        return render(request, "items/update.html", context.model_dump())
    except ItemDoesNotExist:
        logging.warning("Could not find item for update.")
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
    logging.info("Requested to update item via view, retrieving request info...")
    user = request.user
    item_id = request.POST.get("item-id")
    item_name = request.POST.get("item-input")
    store_id = request.POST.get("store-input")
    price = request.POST.get("price-input")
    description = request.POST.get("description-input")

    logging.info("Formatting view input for update on item...")
    try:
        formatted_item_id = int(item_id) if item_id else None
        formatted_store_id = int(store_id) if store_id else None
        formatted_price = float(price) if price else None
    except ValueError:
        logging.error("Retrieved input that could not be formatted for item update.")
        return HttpResponse("Could not format input for item update, please try again.")

    if not item_id or not formatted_item_id:
        logging.error("Item ID is required for an update on an item.")
        return HttpResponse("Could not find ID for update, please try again.", status=404)

    logging.info(
        f"Retrieved request details, attempting to update item with ID: {formatted_item_id}."
    )
    try:
        item = await item_service.update_item(
            user=user,
            item_id=formatted_item_id,
            name=item_name,
            store_id=formatted_store_id,
            price=formatted_price,
            description=description,
        )
        item_dict = item.model_dump()
        item_id = item_dict.get("id")
        return HttpResponseRedirect(f"/items/detail/{item_id}")
    except ItemDoesNotExist:
        logging.error("Item does not exist for update.")
        return HttpResponse(f"Could not find item with ID: {formatted_item_id}.", status=404)
    except ItemAlreadyExists:
        logging.error("Item matching new details already exists, can not update.")
        return HttpResponseRedirect(f"/items/update/{item_id}?error=Item already exists.")


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
    user = request.user
    logging.info(f"User ({user}) requested delete page for item: {item_id}")

    logging.info("Retrieving errors passed to this view...")
    error = request.GET.get("error")

    logging.info("Getting item details and serving page...")
    try:
        item = await item_service.get_item_detail(item_id=item_id)
        context = ItemDetailContext(
            error=error,
            page_title="Delete Item",
            item=item,
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
    logging.info("Requested to delete item via view, retrieving request info...")
    user = request.user
    item_id = request.POST.get("item-id")

    logging.info("Formatting view input for deletion on item...")
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

    logging.info(
        f"Retrieved request details, attempting to delete item with ID: {formatted_item_id}."
    )

    try:
        await item_service.delete_item(user=user, item_id=formatted_item_id)
        return HttpResponseRedirect("/items/me")
    except ItemDoesNotExist:
        logging.error("Item does not exist for deletion.")
        return HttpResponse(f"Could not find item with ID: {formatted_item_id}.", status=404)
