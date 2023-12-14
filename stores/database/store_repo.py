"""Contains store repository functions."""

from datetime import date

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.core.paginator import Paginator

from stores.models import ShoppingStore as Store
from stores.models import ShoppingStorePagination as StorePagination


@sync_to_async
def _filter(
    page_number: int = 1,
    stores_per_page: int = 10,
    name: str | None = None,
    store_types: list[int] | None = None,
    created_on: date | None = None,
    created_before: date | None = None,
    created_after: date | None = None,
    updated_on: date | None = None,
    updated_before: date | None = None,
    updated_after: date | None = None,
    user: User | AnonymousUser | AbstractBaseUser | None = None,
) -> StorePagination:
    """
    Filter stores.

    Args:
        page_number (int): The page number.
        stores_per_page (int): The number of stores per page.
        name (str | None): The name of the store.

    Returns:
        ShoppingStorePagination: Store pagination object.
    """
    stores = Store.objects.all()

    if name:
        stores = stores.filter(name__icontains=name)
    if store_types:
        stores = stores.filter(store_type__in=store_types)
    if created_on:
        stores = stores.filter(created_at__date=created_on)
    if created_before:
        stores = stores.filter(created_at__date__lte=created_before)
    if created_after:
        stores = stores.filter(created_at__date__gte=created_after)
    if updated_on:
        stores = stores.filter(updated_at__date=updated_on)
    if updated_before:
        stores = stores.filter(updated_at__date__lte=updated_before)
    if updated_after:
        stores = stores.filter(updated_at__date__gte=updated_after)
    if user:
        stores = stores.filter(user=user)

    stores = stores.order_by("-updated_at")

    paginator = Paginator(stores, stores_per_page)
    paginated_page = paginator.get_page(page_number)

    paginated_stores = paginated_page.object_list
    results = [store for store in paginated_stores]
    total = paginator.count
    page = paginated_page.number
    total_pages = paginator.num_pages
    has_previous = paginated_page.has_previous()
    previous_page = paginated_page.previous_page_number() if has_previous else None
    has_next = paginated_page.has_next()
    next_page = paginated_page.next_page_number() if has_next else None

    result = StorePagination(
        stores=results,
        total=total,
        page_number=page,
        total_pages=total_pages,
        has_previous=has_previous,
        previous_page=previous_page,
        has_next=has_next,
        next_page=next_page,
    )

    return result


async def create_store(
    name: str,
    store_type: int,
    description: str,
    user: User | AnonymousUser | AbstractBaseUser,
) -> Store:
    """
    Create a store.

    Args:
        name (str): The name of the store.
        store_type (int): The type of the store.
        description (str): The description of the store.
        user (User | AnonymousUser | AbstractBaseUser): The user who created the store.

    Returns:
        ShoppingStore: The created store.
    """
    store = await Store.objects.acreate(
        name=name,
        store_type=store_type,
        description=description,
        user=user,
    )
    await store.asave()
    return store


async def get_stores(
    page_number: int = 1, stores_per_page: int = 10
) -> StorePagination:
    """
    Get all stores.

    Args:
        page (int): The page number.
        stores_per_page (int): The number of stores per page.

    Returns:
        ShoppingStorePagination: Store pagination object.
    """
    return await filter_stores(page_number, stores_per_page)


async def filter_stores(
    page_number: int = 1,
    stores_per_page: int = 10,
    name: str | None = None,
    store_types: list[int] | None = None,
    created_on: date | None = None,
    created_before: date | None = None,
    created_after: date | None = None,
    updated_on: date | None = None,
    updated_before: date | None = None,
    updated_after: date | None = None,
    user: User | AnonymousUser | AbstractBaseUser | None = None,
) -> StorePagination:
    """
    Filter stores.

    Args:
        page_number (int): The page number.
        stores_per_page (int): The number of stores per page.
        name (str | None): The name of the store.

    Returns:
        ShoppingStorePagination: Store pagination object.
    """
    return await _filter(
        page_number,
        stores_per_page,
        name,
        store_types,
        created_on,
        created_before,
        created_after,
        updated_on,
        updated_before,
        updated_after,
        user,
    )
