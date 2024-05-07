"""Contains store repository functions."""

import logging

from datetime import date
from typing import Any, no_type_check

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.core.paginator import Paginator
from django.db.models import Case, Count, F, IntegerField, When

from stores.models import ShoppingStore as Store
from stores.schemas.output import StorePaginationSchema, StoreSchema


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
) -> StorePaginationSchema:
    """
    Filter stores.

    Args:
        page_number (int): The page number.
        stores_per_page (int): The number of stores per page.
        name (str | None): The name of the store.
        store_types (list[int] | None): The store types.
        created_on (date | None): The date the store was created.
        created_before (date | None): The date the store was created before.
        created_after (date | None): The date the store was created after.
        updated_on (date | None): The date the store was updated.
        updated_before (date | None): The date the store was updated before.
        updated_after (date | None): The date the store was updated after.
        user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.

    Returns:
        StorePaginationSchema: Store pagination object.
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
    results = [StoreSchema.from_orm(store) for store in paginated_stores]
    total = paginator.count
    page = paginated_page.number
    total_pages = paginator.num_pages
    has_previous = paginated_page.has_previous()
    previous_page = paginated_page.previous_page_number() if has_previous else None
    has_next = paginated_page.has_next()
    next_page = paginated_page.next_page_number() if has_next else None

    result = StorePaginationSchema(
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
    page_number: int = 1,
    stores_per_page: int = 10,
    user: User | AnonymousUser | AbstractBaseUser | None = None,
) -> StorePaginationSchema:
    """
    Get all stores.

    Args:
        page (int): The page number.
        stores_per_page (int): The number of stores per page.
        user (User): User who owns the stores.

    Returns:
        StorePaginationSchema: Store pagination object.
    """
    return await _filter(page_number, stores_per_page, user=user)


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
) -> StorePaginationSchema:
    """
    Filter stores.

    Args:
        page_number (int): The page number.
        stores_per_page (int): The number of stores per page.
        name (str | None): The name of the store.
        store_types (list[int] | None): The store types.
        created_on (date | None): The date the store was created.
        created_before (date | None): The date the store was created before.
        created_after (date | None): The date the store was created after.
        updated_on (date | None): The date the store was updated.
        updated_before (date | None): The date the store was updated before.
        updated_after (date | None): The date the store was updated after.
        user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.

    Returns:
        StorePaginationSchema: Store pagination object.
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


async def edit_store(
    store_id: int,
    user: User | AnonymousUser | AbstractBaseUser,
    store_name: str | None = None,
    store_type: int | None = None,
    store_description: str | None = None,
) -> Store:
    """
    Edit a store.

    Args:
        store_id (int): The id of the store.
        user (User | AnonymousUser | AbstractBaseUser): The user who created the store.
        store_name (str | None): The new name of the store.
        store_type (int | None): The new type of the store.
        store_description (str | None): The new description of the store.

    Returns:
        ShoppingStore: The edited store.

    Raises:
        Store.DoesNotExist: If the store does not exist.
    """
    store = await Store.objects.aget(id=store_id, user=user)

    if store_name:
        store.name = store_name
    if store_type:
        store.store_type = store_type
    if store_description:
        store.description = store_description

    await store.asave()
    return store


async def delete_store(store_id: int, user: User | AnonymousUser | AbstractBaseUser) -> None:
    """
    Delete a store.

    Args:
        store_id (int): The id of the store.
        user (User | AnonymousUser | AbstractBaseUser): The user who created the store.

    Raises:
        Store.DoesNotExist: If the store does not exist.
    """
    store = await Store.objects.aget(id=store_id, user=user)
    await store.adelete()


async def get_store(store_id: int) -> Store:
    """
    Get a store.

    Args:
        store_id (int): The id of the store.

    Returns:
        ShoppingStore: The store.

    Raises:
        Store.DoesNotExist: If the store does not exist.
    """
    logging.info(f"Retrieving store with ID: {store_id}")
    store = await Store.objects.aget(id=store_id)
    return store


@sync_to_async
@no_type_check
def _pre_aggregate_filter(
    user: User | AnonymousUser | AbstractBaseUser | None = None,
):
    """
    Filter stores by user pre-aggregation.

    Args:
        user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.

    Returns:
        list[ShoppingStore]: The stores.
    """
    stores = Store.objects.all()

    if user:
        stores = stores.filter(user=user)

    return stores


@no_type_check
async def aggregate_stores(
    user: User | AnonymousUser | AbstractBaseUser | None = None,
) -> dict[str, Any]:
    """
    Aggregate stores.

    Args:
        user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.

    Returns:
        dict[str, Any]: The aggregated stores.
    """
    pre_filtered_stores = await _pre_aggregate_filter(user=user)
    result = await pre_filtered_stores.aaggregate(
        online_stores=Count(Case(When(store_type=1, then=1), output_field=IntegerField())),
        in_store_stores=Count(Case(When(store_type=2, then=1), output_field=IntegerField())),
        combined_stores=Count(Case(When(store_type=3, then=1), output_field=IntegerField())),
        total_stores=Count(F("id")),
    )

    return result


async def does_name_exist(name: str) -> bool:
    """
    Check if a store name exists.

    Args:
        name (str): The name of the store.

    Returns:
        bool: True if the store name exists, False otherwise.
    """
    return await Store.objects.filter(name=name).aexists()
