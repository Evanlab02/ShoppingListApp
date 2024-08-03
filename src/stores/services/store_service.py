"""API Service for the stores app."""

import logging
from datetime import date

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database import item_repo
from items.schemas.output import ItemPaginationSchema
from shoppingapp.schemas.shared import DeleteSchema
from stores.constants import STORE_TYPE_MAPPING
from stores.database import store_repo
from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore
from stores.schemas.output import (
    StoreAggregationSchema,
    StorePaginationSchema,
    StoreSchema,
)

log = logging.getLogger(__name__)
log.info("Store service loading...")

STORE_DOES_NOT_EXIST = "Store does not exist."


def _get_store_type_label(store_type_value: int) -> str:
    """
    Get the store type label.

    Args:
        store_type_value (int): The store type value.

    Returns:
        str: The store type label.

    Raises:
        InvalidStoreType: If the store type is invalid.
    """
    log.info("Attempting store type conversion to label.")
    try:
        return STORE_TYPE_MAPPING[store_type_value]
    except KeyError:
        log.warning("Failed store type conversion to label.")
        raise InvalidStoreType(store_type_value)


def _get_store_type_value(store_type_label: str) -> int:
    """
    Get the store type value.

    Args:
        store_type_label (str): The store type label.

    Returns:
        int: The store type value.

    Raises:
        InvalidStoreType: If the store type is invalid.
    """
    log.info("Attempting store type conversion to value.")
    for key, value in STORE_TYPE_MAPPING.items():
        if value == store_type_label:
            return key

    log.warning("Failed store type conversion to value.")
    raise InvalidStoreType(store_type_label)


async def create(new_store: NewStore, user: User | AbstractBaseUser | AnonymousUser) -> StoreSchema:
    """
    Create a new store.

    Args:
        new_store (NewStore): The new store data.

    Returns:
        StoreSchema: The created store.

    Raises:
        InvalidStoreType: If the store type is invalid.
        StoreAlreadyExists: If the store already exists.
    """
    log.info("Retrieving info for new store...")
    name = new_store.name
    store_type = new_store.store_type
    store_type_label = ""
    description = new_store.description

    log.info("Validating store type...")
    if isinstance(store_type, int):
        store_type_label = _get_store_type_label(store_type)
    elif isinstance(store_type, str):
        store_type_label = store_type

    store_type_value = _get_store_type_value(store_type_label)

    log.info("Validating store name...")
    if await store_repo.does_name_exist(name):
        log.warning("Store with this name already exists...")
        raise StoreAlreadyExists(name)

    log.info("Creating store...")
    store = await store_repo.create_store(name, store_type_value, description, user)
    store_schema = StoreSchema.from_orm(store)
    return store_schema


async def get_store_detail(store_id: int) -> StoreSchema:
    """
    Get the store detail.

    Args:
        store_id (int): The id of the store.

    Returns:
        StoreSchema: The store detail.

    Raises:
        StoreDoesNotExist: If the store does not exist.
    """
    try:
        log.info("Getting store details...")
        store = await store_repo.get_store(store_id)
        store_schema = StoreSchema.from_orm(store)
        return store_schema
    except Store.DoesNotExist:
        log.warning(STORE_DOES_NOT_EXIST)
        raise StoreDoesNotExist(store_id)


async def get_store_detail_with_items(
    store_id: int, page_number: int = 1, items_per_page: int = 10
) -> tuple[StoreSchema, ItemPaginationSchema]:
    """
    Get the store detail.

    Args:
        store_id (int): The id of the store.

    Returns:
        StoreSchema: The store detail.

    Raises:
        StoreDoesNotExist: If the store does not exist.
    """
    try:
        log.info("Getting store details with related items...")
        store = await store_repo.get_store(store_id)
        store_schema = StoreSchema.from_orm(store)
        related_items = await item_repo.get_items(
            page=page_number, items_per_page=items_per_page, store=store
        )
        return store_schema, related_items
    except Store.DoesNotExist:
        log.warning(STORE_DOES_NOT_EXIST)
        raise StoreDoesNotExist(store_id)


async def aggregate(
    user: User | AbstractBaseUser | AnonymousUser | None = None,
) -> StoreAggregationSchema:
    """
    Aggregate the stores.

    Returns:
        StoreAggregationSchema: The store aggregation.
    """
    log.info("Aggregating store details...")
    aggregation = await store_repo.aggregate_stores(user)
    result = StoreAggregationSchema.model_validate(aggregation)
    result.combined_online_stores = result.online_stores + result.combined_stores
    result.combined_in_store_stores = result.in_store_stores + result.combined_stores
    return result


async def get_stores(
    limit: int = 10,
    page_number: int = 1,
    user: User | AnonymousUser | AbstractBaseUser | None = None,
) -> StorePaginationSchema:
    """
    Get the stores.

    Args:
        limit (int): The limit of stores per page.
        page_number (int): The page number.
        user (User): User who created the stores.

    Returns:
        StorePaginationSchema: The stores in a paginated format.
    """
    log.info(f"Retrieving stores for page {page_number} with limit {limit}...")
    paginated_stores = await store_repo.get_stores(page_number, limit, user)
    return paginated_stores


async def update_store(
    store_id: int,
    user: User | AnonymousUser | AbstractBaseUser,
    store_name: str | None = None,
    store_type: int | str | None = None,
    store_description: str | None = None,
) -> StoreSchema:
    """
    Update a store with given values.

    Args:
        store_id (int): The store id to update.
        user (User | AnonymousUser | AbstractBaseUser): The user who owns the store.
        store_name (str | None): The new store name, if there is one.
        store_type (str | int | None): The new store type, if there is one.
        store_description (str | None): The new description, if there is one.

    Returns:
        StoreSchema: The store that was edited returned as a schema.

    Raises:
        StoreAlreadyExists: When a store with that name already exists.
        InvalidStoreType: When a invalid store type is given to update to.
    """
    store_type_label = ""
    store_type_value = None

    log.info("Validating store info...")
    if store_name and await store_repo.does_name_exist(store_name):
        log.warning("Store already exists.")
        raise StoreAlreadyExists(store_name)
    elif isinstance(store_type, int):
        store_type_label = _get_store_type_label(store_type)
    elif isinstance(store_type, str):
        store_type_label = store_type

    if store_type and store_type_label:
        store_type_value = _get_store_type_value(store_type_label)

    try:
        log.info("Updating store...")
        store = await store_repo.edit_store(
            store_id=store_id,
            user=user,
            store_name=store_name,
            store_type=store_type_value,
            store_description=store_description,
        )
        store_schema = await sync_to_async(StoreSchema.from_orm)(store)
        return store_schema
    except Store.DoesNotExist:
        log.warning(STORE_DOES_NOT_EXIST)
        raise StoreDoesNotExist(store_id)


async def delete_store(
    store_id: int, user: User | AbstractBaseUser | AnonymousUser
) -> DeleteSchema:
    """
    Delete a store.

    Args:
        store_id (int): The id of the store you wish to delete.
        user (User): The user that owns this store, to prevent users deleting other users stores.

    Returns:
        DeleteSchema: The schema result which contains the result message and details.
    """
    try:
        log.info("Deleting store...")
        await store_repo.delete_store(store_id=store_id, user=user)
        return DeleteSchema(
            message="Deleted Store.", detail=f"Store with ID #{store_id} was deleted."
        )
    except Store.DoesNotExist:
        log.warning(STORE_DOES_NOT_EXIST)
        raise StoreDoesNotExist(store_id=store_id)


async def search_stores(
    page: int = 1,
    limit: int = 10,
    name: str | None = None,
    user: User | AnonymousUser | AbstractBaseUser | None = None,
    ids: list[int] | None = None,
    store_types: list[int] | None = None,
    created_on: date | None = None,
    created_before: date | None = None,
    created_after: date | None = None,
    updated_on: date | None = None,
    updated_before: date | None = None,
    updated_after: date | None = None,
) -> StorePaginationSchema:
    """
    Search for stores based on criteria.

    Args:
        page (int): The page number.
        limit (int): The number of stores per page.
        name (str): Partial or full name of store.
        user (User): The user that owns the store.
        ids (list[int]): List of ids to filter from.
        store_types (list[int]): List of store types to filter from.
        created_on (date): The date the store was created.
        created_before (date): Date the store was created before.
        created_after (date): Date the store was created after.
        updated_on (date): Date the store was last updated.
        updated_before (date): Date the store was last updated before.
        updated_after (date): Date the store was last updated after.

    Returns:
        StorePaginationSchema: The schema result which contains the stores that were searched for.
    """
    log.info(f"PAGE NO - {page}")
    log.info(f"LIMIT - {limit}")
    log.info(f"NAME - {name}")
    log.info(f"STORE TYPES - {store_types}")
    log.info(f"CREATED ON - {created_on}")
    log.info(f"CREATED BEFORE - {created_before}")
    log.info(f"CREATED AFTER - {created_after}")
    log.info(f"UPDATED ON - {updated_on}")
    log.info(f"UPDATED BEFORE - {updated_before}")
    log.info(f"UPDATED AFTER - {updated_after}")
    log.info(f"IDS - {ids}")
    return await store_repo.filter_stores(
        page_number=page,
        stores_per_page=limit,
        name=name,
        user=user,
        store_types=store_types,
        created_on=created_on,
        created_before=created_before,
        created_after=created_after,
        updated_on=updated_on,
        updated_before=updated_before,
        updated_after=updated_after,
        ids=ids,
    )


log.info("Store service loaded.")
