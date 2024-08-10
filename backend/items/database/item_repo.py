"""Contains item repository functions."""

import logging
from typing import Any, no_type_check

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Max, Min, QuerySet, Sum

from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.schemas.output import ItemPaginationSchema, ItemSchema
from stores.models import ShoppingStore as Store

log = logging.getLogger(__name__)
log.info("Item repository loading...")


def _filter(
    name: str | None = None,
    store: Store | None = None,
    stores: list[Store] | None = None,
    user: User | AbstractBaseUser | AnonymousUser | None = None,
    search: ItemSearchSchema | None = None,
) -> QuerySet[Item]:
    """
    Filter items and order them by the updated date.

    Returns a QuerySet of items that match the provided filters.

    Args:
        name (str | None): The name of the item.
        description (str | None): The description of the item.
        price_is (float | None): The price of the item.
        price_is_gt (float | None): The price of the item is greater than.
        price_is_lt (float | None): The price of the item is less than.
        created_on (date | None): The date the item was created.
        created_after (date | None): The date the item was created after.
        created_before (date | None): The date the item was created before.
        updated_on (date | None): The date the item was updated.
        updated_after (date | None): The date the item was updated after.
        updated_before (date | None): The date the item was updated before.
        store (Store | None): The store where the item is stocked.
        user (User | AbstractBaseUser | AnonymousUser | None): The user who created the item.
        ids (list[int] | None): The item ids to filter off of.
        stores (list[Store] | None): The stores to filter off of.

    Returns:
        list[Item]: The filtered items.
    """
    items = Item.objects.all()

    if name:
        items = items.filter(name__icontains=name)
    if store:
        items = items.filter(store=store)
    if stores:
        items = items.filter(store__in=stores)
    if user:
        items = items.filter(user=user)
    if search:
        items = _search(items=items, search=search)

    items = items.order_by("-updated_at")

    return items


def _search(items: QuerySet[Item], search: ItemSearchSchema) -> QuerySet[Item]:
    """
    Search items using the search schema object.

    Args:
        items (QuerySet[Item]): The query set to search upon.
        search (ItemSearchSchema): The search object to use.

    Returns:
        items (QuerySet[Item]): The search result.
    """
    if search.description:
        items = items.filter(description__icontains=search.description)
    if search.price:
        items = items.filter(price=search.price)
    if search.price_is_gt:
        items = items.filter(price__gt=search.price_is_gt)
    if search.price_is_lt:
        items = items.filter(price__lt=search.price_is_lt)
    if search.created_on:
        items = items.filter(created_at__date=search.created_on)
    if search.created_after:
        items = items.filter(created_at__date__gt=search.created_after)
    if search.created_before:
        items = items.filter(created_at__date__lt=search.created_before)
    if search.updated_on:
        items = items.filter(updated_at__date=search.updated_on)
    if search.updated_after:
        items = items.filter(updated_at__date__gt=search.updated_after)
    if search.updated_before:
        items = items.filter(updated_at__date__lt=search.updated_before)
    if search.ids:
        items = items.filter(id__in=search.ids)

    return items


@sync_to_async
def _paginate(
    page_number: int = 1,
    items_per_page: int = 10,
    user: User | AbstractBaseUser | AnonymousUser | None = None,
    store: Store | None = None,
    stores: list[Store] | None = None,
    name: str | None = None,
    search: ItemSearchSchema | None = None,
) -> ItemPaginationSchema:
    """
    Paginate the items.

    Returns a pagination schema with the items.

    Args:
        page_number (int): The page number.
        items_per_page (int): The number of items per page.
        user (User): The user to filter off.
        store (Store): Specific store to filter off.
        name (int): The full or partial name of the item to filter by.
        ids (list[int]): The items to filter off of.
        stores (list[Store]): The stores to filter off.
        created_on (date): The date the store was created on.
        created_before (date): All items created before this date.
        created_after (date): All items created after this date.
        updated_on (date): The date the item was last updated on.
        updated_before (date): All items that were updated before this date.
        updated_after (date): All items that were updated after this date.
        description (str): Full or partial description to filter by.
        price (float): The price of the item.
        price_is_lt (float): Items where the price is less than this.
        price_is_get (float): Items where the price is greater than this.

    Returns:
        ItemPaginationSchema: The paginated items.
    """
    records = _filter(user=user, store=store, name=name, search=search, stores=stores)

    paginator = Paginator(records, items_per_page)
    paginated_page = paginator.get_page(page_number)
    paginated_items = paginated_page.object_list

    items = [ItemSchema.from_orm(record) for record in paginated_items]
    total = paginator.count
    page = paginated_page.number
    total_pages = paginator.num_pages
    has_previous = paginated_page.has_previous()
    previous_page = paginated_page.previous_page_number() if has_previous else None
    has_next = paginated_page.has_next()
    next_page = paginated_page.next_page_number() if has_next else None

    return ItemPaginationSchema(
        items=items,
        total=total,
        page_number=page,
        total_pages=total_pages,
        has_previous=has_previous,
        previous_page=previous_page,
        has_next=has_next,
        next_page=next_page,
    )


async def does_item_exist(name: str, store: Store) -> bool:
    """
    Check if a item exists with the provided details.

    Args:
        name (str): The name of the item.
        store (Store): The store we are checking against.

    Returns:
        bool: True if the item exists, false otherwise.
    """
    item_exists = await Item.objects.filter(name=name, store=store).aexists()
    return item_exists


async def create_item(
    user: User | AbstractBaseUser | AnonymousUser,
    store: Store,
    name: str,
    price: float,
    description: str = "",
) -> Item:
    """
    Create a shopping item.

    Args:
        user (User): The user that created the item.
        store (Store): The store where the item is stocked.
        name (str): The item name.
        price (float): The price of the item.
        description (str): The item description.

    Returns:
        Item: The created item.
    """
    item = await Item.objects.acreate(
        name=name,
        description=description,
        price=price,
        store=store,
        user=user,
    )
    await item.asave()
    return item


async def get_items(
    page: int = 1,
    items_per_page: int = 10,
    user: User | AbstractBaseUser | AnonymousUser | None = None,
    store: Store | None = None,
    name: str | None = None,
    stores: list[Store] | None = None,
    search: ItemSearchSchema | None = None,
) -> ItemPaginationSchema:
    """
    Get all the items.

    Args:
        page (int): The page number.
        items_per_page (int): The number of items per page.

    Returns:
        ItemPaginationSchema: The paginated items.
    """
    items = await _paginate(
        page_number=page,
        items_per_page=items_per_page,
        user=user,
        store=store,
        search=search,
        name=name,
        stores=stores,
    )
    return items


@no_type_check
async def aggregate(user: User | AbstractBaseUser | AnonymousUser | None = None) -> dict[str, Any]:
    """
    Aggregate the items.

    Returns:
        dict[str, Any]: The aggregation of the items.
    """
    filter_items = sync_to_async(_filter)
    items = await filter_items(user=user)

    aggregation = await items.aaggregate(
        total_items=Count("id"),
        total_price=Sum("price"),
        average_price=Avg("price"),
        max_price=Max("price"),
        min_price=Min("price"),
    )

    return aggregation


async def get_item(item_id: int) -> Item:
    """
    Get an item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        Item: The item.
    """
    logging.info(f"Getting item with ID: {item_id}.")
    item = await Item.objects.select_related("store", "user").aget(id=item_id)
    return item


async def get_item_for_user(item_id: int, user: User | AbstractBaseUser | AnonymousUser) -> Item:
    """
    Get an item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        Item: The item.
    """
    item = await Item.objects.select_related("store", "user").aget(id=item_id, user=user)
    return item


async def update_item(
    item: Item,
    name: str | None = None,
    price: float | None = None,
    description: str | None = None,
    store: Store | None = None,
) -> Item:
    """
    Update an item by its ID.

    Args:
        item_id (int): The ID of the item.

    Returns:
        Item: The item.
    """
    if name:
        item.name = name
    if price:
        item.price = price
    if description:
        item.description = description
    if store:
        item.store = store

    logging.info(f"Updating item with ID: {item.id}.")
    await item.asave()
    return item


async def delete_item(item_id: int, user: User | AbstractBaseUser | AnonymousUser) -> None:
    """
    Delete an item by its ID.

    Args:
        item_id (int): The ID of the item.
        user (User | AnonymousUser | AbstractBaseUser): The user who created the item.

    Raises:
        Item.DoesNotExist: If the item does not exist.
    """
    logging.info(f"Retrieving item with ID: '{item_id}' for deletion.")
    item = await Item.objects.aget(id=item_id, user=user)
    logging.info(f"Deleting item with ID: '{item_id}'.")
    await item.adelete()


log.info("Item repository loaded.")
