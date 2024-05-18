"""Contains item service functions."""

import logging

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database import item_repo
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.models import ShoppingItem as Item
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
from shoppingapp.schemas.shared import DeleteSchema
from stores.database import store_repo
from stores.errors.api_exceptions import StoreDoesNotExist
from stores.models import ShoppingStore as Store


async def create_item(
    user: User | AbstractBaseUser | AnonymousUser,
    store_id: int,
    name: str,
    price: float,
    description: str = "",
) -> ItemSchema:
    """
    Create an item.

    Args:
        user (User): The user that created the item.
        store (int): The store id that the item belongs to.
        name (str): The new item name.
        price (float): The price of the item.
        description (str): The description of the item.

    Returns:
        ItemSchema: The item that was created.

    Raises:
        StoreDoesNotExist: If the store id provided is invalid.
        ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
    """
    try:
        store = await store_repo.get_store(store_id=store_id)

        if await item_repo.does_item_exist(name=name, store=store):
            raise ItemAlreadyExists(item_name=name, store_name=store.name)

        item = await item_repo.create_item(
            description=description,
            name=name,
            price=price,
            store=store,
            user=user,
        )
        item_schema = ItemSchema.from_orm(item)
        return item_schema
    except Store.DoesNotExist:
        raise StoreDoesNotExist(store_id=store_id)


async def get_items(
    page: int = 1,
    items_per_page: int = 10,
    user: User | AbstractBaseUser | AnonymousUser | None = None,
) -> ItemPaginationSchema:
    """
    Get all items.

    Returns:
        ItemPaginationSchema: A paginated list of items.
    """
    items = await item_repo.get_items(page=page, items_per_page=items_per_page, user=user)
    return items


async def aggregate(
    user: User | AbstractBaseUser | AnonymousUser | None = None,
) -> ItemAggregationSchema:
    """
    Aggregate the items.

    Returns:
        ItemAggregationSchema: The aggregation of the items.
    """
    aggregation = await item_repo.aggregate(user=user)
    result = ItemAggregationSchema.model_validate(aggregation)
    return result


async def get_item_detail(item_id: int) -> ItemSchema:
    """
    Get an item using the item id.

    Args:
        item_id (int): The item id.

    Returns:
        ItemSchema: The item detail.
    """
    try:
        item = await item_repo.get_item(item_id=item_id)
        logging.info("Item retrieved, converting to schema...")
        item_schema = ItemSchema.from_orm(item)
        return item_schema
    except Item.DoesNotExist:
        logging.warning(f"Item with ID: {item_id} does not exist.")
        raise ItemDoesNotExist(item_id=item_id)


async def _validate_for_update(
    item_id: int,
    user: User | AbstractBaseUser | AnonymousUser,
    name: str | None = None,
    store_id: int | None = None,
) -> tuple[Item, Store | None]:
    """
    Check that all provided details are valid for updating an item.

    Args:
        item_id (int): The item id.
        user (User): The user that created the item.
        name (str): The new item name.
        store_id (int): The store id that the item belongs to.

    Returns:
        tuple[Item, Store | None]: The item and store details, store can be None.

    Raises:
        ItemDoesNotExist: If the item id provided does not exist.
        ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
        StoreDoesNotExist: If the store id provided is invalid.
    """
    logging.info("Validating new updated item details...")
    store = None
    item = None

    if store_id:
        logging.info(f"Getting store with ID: {store_id} (For update on item with ID: {item_id})")
        try:
            store = await store_repo.get_store(store_id=store_id)
        except Store.DoesNotExist:
            raise StoreDoesNotExist(store_id=store_id)

    logging.info("Attempting to retrieve item details...")
    try:
        item = await item_repo.get_item_for_user(item_id=item_id, user=user)
    except Item.DoesNotExist:
        raise ItemDoesNotExist(item_id=item_id)

    logging.info("Checking if item already exists...")
    if name and store and await item_repo.does_item_exist(name=name, store=store):
        raise ItemAlreadyExists(item_name=name, store_name=store.name)

    if name and not store and await item_repo.does_item_exist(name=name, store=item.store):
        raise ItemAlreadyExists(item_name=name, store_name=item.store.name)

    return item, store


async def update_item(
    item_id: int,
    user: User | AbstractBaseUser | AnonymousUser,
    name: str | None = None,
    price: float | None = None,
    description: str | None = None,
    store_id: int | None = None,
) -> ItemSchema:
    """
    Update an item using the item id.

    Args:
        item_id (int): The item id.
        name (str): The new item name.
        price (float): The price of the item.
        description (str): The description of the item.
        store_id (int): The store id that the item belongs to.

    Returns:
        ItemSchema: The item details.

    Raises:
        ItemDoesNotExist: If the item id provided does not exist.
        ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
        StoreDoesNotExist: If the store id provided is invalid.
    """
    item, store = await _validate_for_update(
        item_id=item_id, user=user, name=name, store_id=store_id
    )

    logging.info("Update checks passed.")
    item = await item_repo.update_item(
        item=item,
        name=name,
        price=price,
        description=description,
        store=store,
    )
    item_schema = ItemSchema.from_orm(item)
    return item_schema


async def delete_item(item_id: int, user: User | AbstractBaseUser | AnonymousUser) -> DeleteSchema:
    """
    Delete an item using the item id.

    Args:
        item_id (int): The item id.
        user (User): The user that created the item.

    Returns:
        DeleteSchema: The deletion result.
    """
    try:
        await item_repo.delete_item(item_id=item_id, user=user)
        return DeleteSchema(message="Deleted Item.", detail=f"Item with ID #{item_id} was deleted.")
    except Item.DoesNotExist:
        logging.warning(f"Item with ID: {item_id} does not exist for user: {user}. (For deletion)")
        raise ItemDoesNotExist(item_id=item_id)
