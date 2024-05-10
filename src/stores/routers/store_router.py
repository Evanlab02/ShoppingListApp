"""Contains store router functions."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from shoppingapp.schemas.shared import DeleteSchema
from stores.constants import STORE_TYPE_MAPPING
from stores.schemas.input import NewStore, StoreDescription
from stores.schemas.output import (
    StoreAggregationSchema,
    StorePaginationSchema,
    StoreSchema,
)
from stores.services import store_service

store_router = Router(tags=["Stores"], auth=ApiKey())


@store_router.post("/create", response={201: StoreSchema})
async def create_store(request: HttpRequest, new_store: NewStore) -> StoreSchema:
    """
    Create a new store.

    Args:
        request (HttpRequest): The HTTP request.
        new_store (NewStore): The new store data.

    Returns:
        StoreSchema: The created store.
    """
    user = request.user
    store = await store_service.create(new_store, user)
    return store


@store_router.get("/types/mapping")
async def get_mapping(request: HttpRequest) -> dict[int, str]:
    """
    Get the store types mapping.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        dict[int, str]: The mapping.
    """
    return STORE_TYPE_MAPPING


@store_router.get("/detail/{store_id}", response={200: StoreSchema})
async def get_store_detail(request: HttpRequest, store_id: int) -> StoreSchema:
    """
    Get the store details.

    Args:
        request (HttpRequest): The HTTP request.
        store_id (int): The store ID.

    Returns:
        StoreSchema: The store details.
    """
    store = await store_service.get_store_detail(store_id)
    return store


@store_router.get("/aggregate", response={200: StoreAggregationSchema})
async def get_store_aggregation(request: HttpRequest) -> StoreAggregationSchema:
    """
    Get the store aggregation.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StoreAggregationSchema: The store aggregation.
    """
    result = await store_service.aggregate()
    return result


@store_router.get("/aggregate/me", response={200: StoreAggregationSchema})
async def get_store_aggregation_by_user(request: HttpRequest) -> StoreAggregationSchema:
    """
    Get the store aggregation by user.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StoreAggregationSchema: The store aggregation by user.
    """
    user = request.user
    result = await store_service.aggregate(user=user)
    return result


@store_router.get("", response={200: StorePaginationSchema})
async def get_stores(request: HttpRequest, limit: int = 10, page: int = 1) -> StorePaginationSchema:
    """
    Get the stores.

    Args:
        request (HttpRequest): The HTTP request.
        limit (int): The limit of stores to get per page.
        page (int): The page number.

    Returns:
        StorePaginationSchema: The stores.
    """
    result = await store_service.get_stores(limit, page)
    return result


@store_router.get("/me", response={200: StorePaginationSchema})
async def get_personal_stores(
    request: HttpRequest, limit: int = 10, page: int = 1
) -> StorePaginationSchema:
    """
    Get the stores you have created.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StorePaginationSchema: The stores.
    """
    user = request.user
    result = await store_service.get_stores(limit, page, user)
    return result


@store_router.patch("/update/{store_id}", response={200: StoreSchema})
async def update_store(
    request: HttpRequest,
    store_id: int,
    description: StoreDescription | None = None,
    name: str | None = None,
    store_type: str | None = None,
) -> StoreSchema:
    """
    Update the store.

    Args:
        request (HttpRequest): The HTTP request.
        store_id (int): The store id, the one you want to update.
        description (StoreDescription | None): Payload containing updated description.
        name (str | None): The new name of the store.
        store_type (str | None): The new store type.

    Returns:
        StoreSchema: The schema for the updated store.
    """
    formatted_type: int | str | None = None
    new_description = description.description if description else None

    try:
        formatted_type = int(store_type) if store_type else None
    except ValueError:
        formatted_type = store_type

    user = request.user
    result = await store_service.update_store(store_id, user, name, formatted_type, new_description)
    return result


@store_router.delete("/delete/{store_id}", response={200: DeleteSchema})
async def delete_store(
    request: HttpRequest,
    store_id: int,
) -> DeleteSchema:
    """
    Delete a store.

    Delete the store that has the provided id.

    Args:
        request (HttpRequest): The request.
        store_id (int): The store id provided, for deletion.

    Returns:
        DeleteSchema: The result schema.

    Raises:
        StoreDoesNotExist: If there store_id is invalid or you do not own the store.
    """
    user = request.user
    result = await store_service.delete_store(store_id=store_id, user=user)
    return result
