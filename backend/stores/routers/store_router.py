"""Contains store router."""

import logging
from typing import Literal

from django.http import HttpRequest
from ninja import Router

from authentication.auth import TOKEN_AUTH
from shoppingapp.schemas.shared import DeleteSchema, ErrorSchema
from stores.constants import STORE_TYPE_MAPPING
from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore, StorePatch, StoreSearch, StoreUpdate
from stores.schemas.output import (
    StoreAggregationSchema,
    StorePaginationSchema,
    StoreSchema,
)
from stores.services.store_service import StoreService

store_router = Router(tags=["Stores"], auth=TOKEN_AUTH)

log = logging.getLogger(__name__)

SERVICE = StoreService()


@store_router.get(
    "/types/mapping",
    response={200: dict[int, str], 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_types_mapping",
)
async def get_mapping(request: HttpRequest) -> dict[int, str]:
    """
    Get the store types mapping.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        dict[int, str]: The mapping.
    """
    return STORE_TYPE_MAPPING


@store_router.post(
    "",
    response={201: StoreSchema, 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_create",
)
async def create_store(request: HttpRequest, new_store: NewStore) -> tuple[int, Store]:
    """
    Create a new store.

    Args:
        request (HttpRequest): The HTTP request.
        new_store (NewStore): The new store data.

    Returns:
        StoreSchema: The created store.
    """
    user = await request.auser()
    store = await SERVICE.create(new_store, user)
    return 201, store


@store_router.get(
    "",
    response={
        200: StorePaginationSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_get",
)
async def get_stores(
    request: HttpRequest,
    limit: int = 10,
    page: int = 1,
    sort: Literal["name", "created_on", "updated_on"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> StorePaginationSchema:
    """
    Get the stores.

    Args:
        request (HttpRequest): The HTTP request.
        limit (int): The limit of stores to get per page.
        page (int): The page number.
        sort (str | None): The field to sort by.
        sort_dir (str | None): The direction to sort in.

    Returns:
        StorePaginationSchema: The stores.
    """
    return await SERVICE.get_stores(limit, page, sort=sort, sort_dir=sort_dir)


@store_router.get(
    "/me",
    response={200: StorePaginationSchema, 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_get_me",
)
async def get_personal_stores(
    request: HttpRequest,
    limit: int = 10,
    page: int = 1,
    sort: Literal["name", "created_on", "updated_on"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> StorePaginationSchema:
    """
    Get the stores you have created.

    Args:
        request (HttpRequest): The HTTP request.
        limit (int): The limit of stores to get per page.
        page (int): The page number.
        sort (str | None): The field to sort by.
        sort_dir (str | None): The direction to sort in.

    Returns:
        StorePaginationSchema: The stores.
    """
    user = await request.auser()
    return await SERVICE.get_stores(limit, page, user, sort, sort_dir)


@store_router.post(
    "/search",
    response={200: StorePaginationSchema, 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_search",
)
async def search(
    request: HttpRequest,
    filters: StoreSearch,
    page: int = 1,
    limit: int = 10,
    sort: Literal["name", "created_on", "updated_on"] | None = None,
    sort_dir: Literal["asc", "desc"] | None = None,
) -> StorePaginationSchema:
    """
    Perform search for stores.

    Args:
        request (HttpRequest): The HTTP request to the API.
        filters (StoreSearch): The body containing the filters.
        page (int): The page number.
        limit (int): The number of stores per page.
        sort (str | None): The field to sort by.
        sort_dir (str | None): The direction to sort in.

    Returns:
        StorePaginationSchema: The stores in a paginated response.
    """
    user = None
    if filters.own:
        user = await request.auser()

    return await SERVICE.search_stores(
        page_number=page,
        stores_per_page=limit,
        name=filters.name,
        user=user,  # type: ignore
        search=filters,
        sort=sort,
        sort_dir=sort_dir,
    )


@store_router.get(
    "/aggregate",
    response={200: StoreAggregationSchema, 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_aggregate",
)
async def get_store_aggregation(request: HttpRequest) -> StoreAggregationSchema:
    """
    Get the store aggregation.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StoreAggregationSchema: The store aggregation.
    """
    return await SERVICE.aggregate()


@store_router.get(
    "/aggregate/me",
    response={200: StoreAggregationSchema, 400: ErrorSchema, 401: ErrorSchema, 500: ErrorSchema},
    url_name="store_aggregate_me",
)
async def get_store_aggregation_by_user(request: HttpRequest) -> StoreAggregationSchema:
    """
    Get the store aggregation by user.

    Args:
        request (HttpRequest): The HTTP request.

    Returns:
        StoreAggregationSchema: The store aggregation by user.
    """
    user = await request.auser()
    return await SERVICE.aggregate(user=user)


@store_router.get(
    "/{store_id}",
    response={
        200: StoreSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_get_detail",
)
async def get_store_detail(request: HttpRequest, store_id: int) -> Store:
    """
    Get the store details.

    Args:
        request (HttpRequest): The HTTP request.
        store_id (int): The store ID.

    Returns:
        StoreSchema: The store details.
    """
    return await SERVICE.get_store(store_id)


@store_router.patch(
    "/{store_id}",
    response={
        200: StoreSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_patch",
)
async def patch_store(
    request: HttpRequest,
    store_id: int,
    patch: StorePatch,
) -> Store:
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
    user = await request.auser()
    return await SERVICE.update(store_id, user, patch.name, patch.store_type, patch.description)


@store_router.put(
    "/{store_id}",
    response={
        200: StoreSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_put",
)
async def update_store(
    request: HttpRequest,
    store_id: int,
    update: StoreUpdate,
) -> Store:
    """
    Update the store.

    Args:
        request (HttpRequest): The HTTP request.
        store_id (int): The store id, the one you want to update.
        update (StoreUpdate): The update payload.

    Returns:
        StoreSchema: The schema for the updated store.
    """
    user = await request.auser()
    return await SERVICE.update(store_id, user, update.name, update.store_type, update.description)


@store_router.delete(
    "/{store_id}",
    response={
        200: DeleteSchema,
        400: ErrorSchema,
        401: ErrorSchema,
        404: ErrorSchema,
        500: ErrorSchema,
    },
    url_name="store_delete",
)
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
    user = await request.auser()
    await SERVICE.delete(store_id, user)
    return DeleteSchema(
        message="Store deleted successfully",
        detail=f"Store with id #{store_id} has been deleted.",
    )
