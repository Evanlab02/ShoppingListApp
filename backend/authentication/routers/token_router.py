"""Contains authentication routes."""

import logging

from django.http import HttpRequest
from ninja import Router

from authentication.auth import SESSION_AUTH
from authentication.schemas.output import TokenResponse
from authentication.services.api.client_service import ClientService

log = logging.getLogger(__name__)
token_router = Router(tags=["Token"], auth=SESSION_AUTH)
service = ClientService()


@token_router.get("", response={200: TokenResponse}, url_name="auth_token")
async def get_token(request: HttpRequest) -> TokenResponse:
    """
    Get a token.

    Args:
        request (HttpRequest): The request object

    Returns:
        GeneralResponse: The response object with the token
    """
    user = await request.auser()
    token, secret = await service.get_token(user)
    return TokenResponse(token=token, secret=secret)
