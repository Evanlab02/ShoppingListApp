"""API Service for the stores app."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.constants import STORE_TYPE_MAPPING
from stores.database import store_repo
from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore
from stores.schemas.output import StoreAggregationSchema, StoreSchema, UserSchema


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
    try:
        return STORE_TYPE_MAPPING[store_type_value]
    except KeyError:
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
    for key, value in STORE_TYPE_MAPPING.items():
        if value == store_type_label:
            return key

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
    name = new_store.name
    store_type = new_store.store_type
    store_type_label = ""
    description = new_store.description

    if isinstance(store_type, int):
        store_type_label = _get_store_type_label(store_type)
    elif isinstance(store_type, str):
        store_type_label = store_type

    if await store_repo.does_name_exist(name):
        raise StoreAlreadyExists(name)

    store_type_value = _get_store_type_value(store_type_label)
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
        store = await store_repo.get_store(store_id)
        user = await sync_to_async(lambda: store.user)()
        user_schema = UserSchema.from_orm(user)
        store_schema = StoreSchema.from_orm(store)
        store_schema.user = user_schema
        return store_schema
    except Store.DoesNotExist:
        raise StoreDoesNotExist(store_id)


async def aggregate(
    user: User | AbstractBaseUser | AnonymousUser | None = None,
) -> StoreAggregationSchema:
    """
    Aggregate the stores.

    Returns:
        StoreAggregationSchema: The store aggregation.
    """
    aggregation = await store_repo.aggregate_stores(user)
    result = StoreAggregationSchema.model_validate(aggregation)
    result.combined_online_stores = result.online_stores + result.combined_stores
    result.combined_in_store_stores = result.in_store_stores + result.combined_stores
    return result
