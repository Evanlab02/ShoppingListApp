"""Contains store router functions."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from stores.constants import STORE_TYPE_MAPPING
from stores.schemas.input import NewStore
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
async def get_personal_stores(request: HttpRequest) -> StorePaginationSchema:
    """
    Get the stores you have created.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StorePaginationSchema: The stores.
    """
    result = await store_service.get_stores()
    return result
