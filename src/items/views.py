"""Contains the views for the items app."""

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from authentication.decorators.login import async_login_required
from items.errors.exceptions import ItemAlreadyExists
from items.schemas.contexts import ItemCreateContext
from items.services import item_service
from stores.services import store_service

CREATE_PAGE = "create"
CREATE_ACTION = "create/action"


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
