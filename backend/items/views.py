"""Contains the views for the items app."""

import logging

from django.http import Http404, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from authentication.decorators.login import async_login_required, login_required
from items.errors.exceptions import ItemDoesNotExist
from items.forms.item import ItemForm
from items.models import ShoppingItem as Item
from items.schemas.contexts import ItemDetailContext, ItemOverviewContext
from items.schemas.output import ItemSchema
from items.services.item_service import ItemService
from shoppingapp.schemas import BaseContext
from shoppingapp.utilities.utils import get_overview_params
from stores.services.store_service import StoreService

CREATE_PAGE = "create"
OVERVIEW_PAGE = ""
PERSONALIZED_OVERVIEW_PAGE = "me"
DETAIL_PAGE = "detail/<int:item_id>"
UPDATE_PAGE = "update/<int:item_id>"
DELETE_PAGE = "delete/<int:item_id>"

log = logging.getLogger(__name__)

SERVICE = ItemService()
STORE_SERVICE = StoreService()

ITEM_404_ERROR = "Item does not exist."


@require_http_methods(["GET", "POST"])
@login_required
def create_page(request: HttpRequest) -> HttpResponse:
    """
    Render the create page.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: The response object.
    """
    if request.method == "POST":
        form = ItemForm(request.POST, user=request.user)
        if form.is_valid():
            item = form.save()
            url = reverse("item_detail_page", kwargs={"item_id": item.id})
            return HttpResponseRedirect(url)
    else:
        form = ItemForm(user=request.user)

    context = BaseContext(page_title="Create Item")
    return render(request, "items/create.html", context.attach_form(form))


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
        raise Http404(ITEM_404_ERROR)


@require_http_methods(["GET", "POST"])
@login_required
def update_page(request: HttpRequest, item_id: int) -> HttpResponse:
    """
    Render the update page.

    TODO: Need to create sync services to use in these views.

    Args:
        request (HttpRequest): The request object.
        item_id (int): The item id.

    Returns:
        HttpResponse: The response object.
    """
    try:
        user = request.user
        item = Item.objects.get(id=item_id, user=user)  # type: ignore

        if request.method == "POST":
            form = ItemForm(request.POST, user=user, instance=item)
            if form.is_valid():
                item = form.save()
                url = reverse("item_detail_page", kwargs={"item_id": item.id})
                return HttpResponseRedirect(url)
        else:
            form = ItemForm(user=user, instance=item)

        context = BaseContext(page_title="Update Item")
        return render(request, "items/update.html", context.attach_form(form))
    except Item.DoesNotExist:
        raise Http404(ITEM_404_ERROR)


@require_http_methods(["GET", "POST"])
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
    try:
        user = await request.auser()
        error = request.GET.get("error")

        if request.method == "POST":
            await SERVICE.delete_item(user=user, item_id=item_id)
            return HttpResponseRedirect(f"{reverse('item_personalized_overview_page')}")
        else:
            item = await SERVICE.get_item_for_user(item_id=item_id, user=user)
            context = ItemDetailContext(
                error=error,
                page_title="Delete Item",
                item=ItemSchema.from_orm(item),
            )
            return render(request, "items/delete.html", context.model_dump())
    except ItemDoesNotExist:
        logging.error("Could not find item for deletion.")
        raise Http404(ITEM_404_ERROR)
