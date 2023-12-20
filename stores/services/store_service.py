"""API Service for the stores app."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.constants import STORE_TYPE_MAPPING
from stores.database.store_repo import create_store, does_name_exist
from stores.errors.api_exceptions import InvalidStoreType, StoreAlreadyExists
from stores.schemas.input import NewStore
from stores.schemas.output import StoreSchema


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


async def create(
    new_store: NewStore, user: User | AbstractBaseUser | AnonymousUser
) -> StoreSchema:
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

    if await does_name_exist(name):
        raise StoreAlreadyExists(name)

    store_type_value = _get_store_type_value(store_type_label)
    store = await create_store(name, store_type_value, description, user)

    store_type_label = _get_store_type_label(store.store_type)
    store_schema = StoreSchema(
        id=store.id,
        name=store.name,
        store_type=store_type_label,
        description=store.description,
    )

    return store_schema
