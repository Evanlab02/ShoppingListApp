"""Contains item service functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database import item_repo
from items.errors.exceptions import ItemAlreadyExists
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
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
