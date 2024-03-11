"""Contains item repository functions."""

from django.contrib.auth.models import User

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


async def create_item(
    user: User, store: Store, name: str, price: float, description: str = ""
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
