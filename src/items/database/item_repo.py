"""Contains item repository functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


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
