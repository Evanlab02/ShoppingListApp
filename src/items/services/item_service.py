"""Contains item service functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database import item_repo
from items.schemas.output import ItemSchema
from stores.models import ShoppingStore as Store


async def create_item(user: User | AbstractBaseUser | AnonymousUser, store: Store) -> ItemSchema:
    """
    Create an item.

    Args:
        user (User): The user that created the item.
        store (Store): The store that the item belongs to.

    Returns:
        Item: The item that was created.
    """
    item = await item_repo.create_item(
        description="Gaming headphones created for gamers designed by gamers.",
        name="Logitech G Pro X",
        price=2500,
        store=store,
        user=user,
    )
    item_schema = ItemSchema.from_orm(item)
    return item_schema
