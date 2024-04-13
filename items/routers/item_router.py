"""Contains item router functions."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from items.schemas.input import NewItem
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
from items.services import item_service

item_router = Router(tags=["Items"], auth=ApiKey())


@item_router.post("/create", response={201: ItemSchema})
async def create_item(request: HttpRequest, new_item: NewItem) -> ItemSchema:
    """
    Create a new item.

    Args:
        request (HttpRequest): The HTTP request.
        new_item (NewItem): The new item data.

    Returns:
        ItemSchema: The created item.
    """
    user = request.user
    store_id = new_item.store_id
    item_name = new_item.name
    item_price = new_item.price
    item_description = new_item.description
    item = await item_service.create_item(
        user=user,
        store_id=store_id,
        name=item_name,
        price=item_price,
        description=item_description,
    )
    return item


@item_router.get("", response={200: ItemPaginationSchema})
async def get_items(
    request: HttpRequest, page: int = 1, per_page: int = 10
) -> ItemPaginationSchema:
    """
    Get all items.

    Args:
        request (HttpRequest): The HTTP request.
        page (int): The page number.
        per_page (int): The number of items per page.

    Returns:
        ItemPaginationSchema: The paginated list of items.
    """
    items = await item_service.get_items(page=page, items_per_page=per_page)
    return items


@item_router.get("/me", response={200: ItemPaginationSchema})
async def get_my_items(
    request: HttpRequest, page: int = 1, per_page: int = 10
) -> ItemPaginationSchema:
    """
    Get all items.

    Args:
        request (HttpRequest): The HTTP request.
        page (int): The page number.
        per_page (int): The number of items per page.

    Returns:
        ItemPaginationSchema: The paginated list of items.
    """
    user = request.user
    items = await item_service.get_items(page=page, items_per_page=per_page, user=user)
    return items


@item_router.get("/aggregate", response={200: ItemAggregationSchema})
async def aggregate(request: HttpRequest) -> ItemAggregationSchema:
    """
    Get the aggregation of all items.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        ItemAggregationSchema: The aggregation of all items.
    """
    aggregation = await item_service.aggregate()
    return aggregation
