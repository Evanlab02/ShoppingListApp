"""Contains item service functions."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database import item_repo
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.models import ShoppingItem as Item
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
from shoppingapp.schemas.shared import UserSchema
from stores.database import store_repo
from stores.errors.api_exceptions import StoreDoesNotExist
from stores.models import ShoppingStore as Store
from stores.schemas.output import StoreSchemaNoUser


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
        user = await sync_to_async(lambda: item.user)()
        store = await sync_to_async(lambda: item.store)()

        user_schema = UserSchema.from_orm(user)
        store_schema = StoreSchemaNoUser.from_orm(store)
        item_schema = ItemSchema.from_orm(item)

        item_schema.store = store_schema
        item_schema.user = user_schema

        return item_schema
    except Item.DoesNotExist:
        raise ItemDoesNotExist(item_id=item_id)


async def update_item(item_id: int) -> ItemSchema:
    """
    Update an item using the item id.

    Args:
        item_id (int): The item id.

    Returns:
        ItemSchema: The item details.

    Raises:
        ItemDoesNotExist: If the item id provided does not exist.
    """
    try:
        item = await item_repo.update_item(item_id=item_id)
        item_schema = ItemSchema.from_orm(item)
        return item_schema
    except Item.DoesNotExist:
        raise ItemDoesNotExist(item_id=item_id)
