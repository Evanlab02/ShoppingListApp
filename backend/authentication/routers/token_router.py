"""Contains authentication routes."""

import logging

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from authentication.schemas.output import GeneralResponse
from authentication.services.api import client_service as service
log = logging.getLogger(__name__)
token_router = Router(tags=["Token"], auth=ApiKey())


@token_router.get("", response={200: GeneralResponse})
async def get_token(request: HttpRequest) -> GeneralResponse:
    """
    Get a token.

    Args:
        request (HttpRequest): The request object

    Returns:
        GeneralResponse: The response object with the token
    """
    user = await request.auser()
    token = await service.get_token(user, request.headers.get("X-API-Key"))
    return GeneralResponse(message="Token retrieved.", detail=token)
