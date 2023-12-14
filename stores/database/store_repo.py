"""Contains store repository functions."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore


async def create_store(
    name: str,
    store_type: int,
    description: str,
    user: User | AnonymousUser | AbstractBaseUser,
) -> ShoppingStore:
    """
    Create a store.

    Args:
        name (str): The name of the store.
        store_type (int): The type of the store.
        description (str): The description of the store.
        username (str): The username of the user creating the store.

    Returns:
        ShoppingStore: The created store.
    """
    store = await ShoppingStore.objects.acreate(
        name=name,
        store_type=store_type,
        description=description,
        user=user,
    )
    await store.asave()
    return store
