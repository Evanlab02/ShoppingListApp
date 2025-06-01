"""Contains item router functions."""

import logging
from typing import Literal

from django.http import HttpRequest
from ninja import Router

from authentication.auth import TOKEN_AUTH
from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema, NewItem, PatchItem, UpdateItem
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
from items.services.item_service import ItemService
from shoppingapp.schemas.shared import DeleteSchema

log = logging.getLogger(__name__)

item_router = Router(tags=["Items"], auth=TOKEN_AUTH)
item_service = ItemService()


@item_router.post("", response={201: ItemSchema}, url_name="item_create")
async def create_item(request: HttpRequest, new_item: NewItem) -> ItemSchema:
    """
    Create a new item.

    Args:
        request (HttpRequest): The HTTP request.
        new_item (NewItem): The new item data.

    Returns:
        ItemSchema: The created item.
    """
    user = await request.auser()
    item = await item_service.create_item(
        user=user,
        store_id=new_item.store_id,
        name=new_item.name,
        price=new_item.price,
        description=new_item.description,
    )
    await item.astore()
    return ItemSchema.from_orm(item)


@item_router.get("", response={200: ItemPaginationSchema}, url_name="item_list")
async def get_items(
    request: HttpRequest,
    page: int = 1,
    per_page: int = 10,
    sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> ItemPaginationSchema:
    """
    Get all items.

    Args:
        request (HttpRequest): The HTTP request.
        page (int): The page number.
        per_page (int): The number of items per page.
        sort (str): The field to sort by.
        sort_dir (str): The direction to sort in, default is 'desc'.

    Returns:
        ItemPaginationSchema: The paginated list of items.
    """
    return await item_service.get_items(
        page=page, items_per_page=per_page, sort=sort, sort_dir=sort_dir
    )


@item_router.get("/me", response={200: ItemPaginationSchema}, url_name="item_list_me")
async def get_my_items(
    request: HttpRequest,
    page: int = 1,
    per_page: int = 10,
    sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> ItemPaginationSchema:
    """
    Get all items.

    Args:
        request (HttpRequest): The HTTP request.
        page (int): The page number.
        per_page (int): The number of items per page.
        sort (str): The field to sort by.
        sort_dir (str): The direction to sort in, default is 'desc'.

    Returns:
        ItemPaginationSchema: The paginated list of items.
    """
    user = await request.auser()
    return await item_service.get_items(
        page=page, items_per_page=per_page, user=user, sort=sort, sort_dir=sort_dir
    )


@item_router.get("/aggregate", response={200: ItemAggregationSchema}, url_name="item_aggregate")
async def aggregate(request: HttpRequest) -> ItemAggregationSchema:
    """
    Get the aggregation of all items.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        ItemAggregationSchema: The aggregation of all items.
    """
    return await item_service.aggregate()


@item_router.get(
    "/aggregate/me", response={200: ItemAggregationSchema}, url_name="item_aggregate_me"
)
async def aggregate_my_items(request: HttpRequest) -> ItemAggregationSchema:
    """
    Get the aggregation of personal items.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        ItemAggregationSchema: The aggregation of personal items.
    """
    user = await request.auser()
    return await item_service.aggregate(user=user)


@item_router.post("/search", response={200: ItemPaginationSchema}, url_name="item_search")
async def search(
    request: HttpRequest,
    search: ItemSearchSchema,
    page: int = 1,
    limit: int = 10,
    name: str | None = None,
    own: bool = False,
    store: int | None = None,
    sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> ItemPaginationSchema:
    """Search for items based off filters."""
    user = None
    if own:
        user = await request.auser()

    return await item_service.search_items(
        user=user,
        limit=limit,
        name=name,
        page=page,
        search=search,
        store_id=store,
        sort=sort,
        sort_dir=sort_dir,
    )


@item_router.get("/{item_id}", response={200: ItemSchema}, url_name="item_detail")
async def get_item_detail(request: HttpRequest, item_id: int) -> Item:
    """
    Get an item detail.

    Args:
        request (HttpRequest): The HTTP request.
        item_id (int): The item id.

    Returns:
        ItemSchema: The item detail.
    """
    return await item_service.get_item_detail(item_id=item_id)


@item_router.patch("/{item_id}", response={200: ItemSchema}, url_name="item_patch")
async def patch_item(request: HttpRequest, item_id: int, item_schema: PatchItem) -> Item:
    """
    Patch an item.

    Args:
        request (HttpRequest): The HTTP request.
        item_id (int): The item id.
        item_schema (PatchItem): The item data to patch.

    Returns:
        ItemSchema: The patched item.
    """
    user = await request.auser()
    item = await item_service.update_item(
        item_id=item_id,
        user=user,
        new_store_id=item_schema.store_id,
        new_name=item_schema.name,
        new_price=item_schema.price,
        new_description=item_schema.description,
    )
    await item.auser()
    await item.astore()
    return item


@item_router.put("/{item_id}", response={200: ItemSchema}, url_name="item_update")
async def update_item(request: HttpRequest, item_id: int, item_schema: UpdateItem) -> Item:
    """
    Update an item.

    Args:
        request (HttpRequest): The HTTP request.
        item_id (int): The item id.
        item_schema (UpdateItem): The item data to update.

    Returns:
        ItemSchema: The updated item.
    """
    user = await request.auser()
    item = await item_service.update_item(
        item_id=item_id,
        user=user,
        new_store_id=item_schema.store_id,
        new_name=item_schema.name,
        new_price=item_schema.price,
        new_description=item_schema.description,
    )
    await item.auser()
    await item.astore()
    return item


@item_router.delete("/{item_id}", response={200: DeleteSchema}, url_name="item_delete")
async def delete_item(request: HttpRequest, item_id: int) -> DeleteSchema:
    """
    Delete an item.

    Args:
        request (HttpRequest): The HTTP request.
        item_id (int): The item id.

    Returns:
        DeleteSchema: The delete schema.
    """
    user = await request.auser()
    return await item_service.delete_item(item_id=item_id, user=user)
