"""Contains authentication routes."""

from django.http import HttpRequest
from ninja import Router

from authentication.schemas.input import NewUser
from authentication.schemas.output import GeneralResponse
from authentication.services.api.user_service import register_user

auth_router = Router()


@auth_router.post("/register", response={201: GeneralResponse})
async def register(request: HttpRequest, new_user: NewUser) -> GeneralResponse:
    """
    Register a new user.

    Args:
        request (HttpRequest): The request object
        new_user (NewUser): The new user data

    Returns:
        GeneralResponse: The response object
    """
    user = request.user
    response = await register_user(user, new_user)
    return response
