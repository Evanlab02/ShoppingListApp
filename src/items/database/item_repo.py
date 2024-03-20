"""Contains item repository functions."""

from datetime import date

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import QuerySet

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


async def _filter(
    name: str | None = None,
    description: str | None = None,
    price_is: float | None = None,
    price_is_gt: float | None = None,
    price_is_lt: float | None = None,
    created_on: date | None = None,
    created_after: date | None = None,
    created_before: date | None = None,
    updated_on: date | None = None,
    updated_after: date | None = None,
    updated_before: date | None = None,
    store: Store | None = None,
    user: User | AbstractBaseUser | AnonymousUser | None = None,
) -> QuerySet[Item]:
    """
    Filter items.

    Returns:
        list[Item]: The filtered items.
    """
    items = Item.objects.all()

    if name:
        items = items.filter(name__icontains=name)
    if description:
        items = items.filter(description__icontains=description)
    if price_is:
        items = items.filter(price=price_is)
    if price_is_gt:
        items = items.filter(price__gt=price_is_gt)
    if price_is_lt:
        items = items.filter(price__lt=price_is_lt)
    if created_on:
        items = items.filter(created_at__date=created_on)
    if created_after:
        items = items.filter(created_at__date__gt=created_after)
    if created_before:
        items = items.filter(created_at__date__lt=created_before)
    if updated_on:
        items = items.filter(updated_at__date=updated_on)
    if updated_after:
        items = items.filter(updated_at__date__gt=updated_after)
    if updated_before:
        items = items.filter(updated_at__date__lt=updated_before)
    if store:
        items = items.filter(store=store)
    if user:
        items = items.filter(user=user)

    return items


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
