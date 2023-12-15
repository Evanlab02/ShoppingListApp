"""Contains store router functions."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from stores.schemas.input import NewStore
from stores.schemas.output import StoreSchema
from stores.services.api.store_service import create

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
    store = await create(new_store, user)
    return store
