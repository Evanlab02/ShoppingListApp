"""Contains authentication routes."""

from django.http import HttpRequest
from ninja import Router

from authentication.schemas.input import NewUser, UserCredentials
from authentication.schemas.output import GeneralResponse
from authentication.services.api.user_service import (
    get_token,
    login,
    logout,
    register_user,
)

auth_router = Router(tags=["Authentication"])


@auth_router.post("/login", response={200: GeneralResponse})
def login_user(request: HttpRequest, user_creds: UserCredentials) -> GeneralResponse:
    """
    Login a user.

    Args:
        request (HttpRequest): The request object
        user_details (UserCredentials): The user credentials

    Returns:
        GeneralResponse: The response object
    """
    response = login(request, user_creds.username, user_creds.password)
    return response


@auth_router.post("/logout", response={200: GeneralResponse})
def logout_user(request: HttpRequest) -> GeneralResponse:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request object

    Returns:
        GeneralResponse: The response object
    """
    response = logout(request)
    return response


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


@auth_router.get("/token", response={200: GeneralResponse})
def token(request: HttpRequest) -> GeneralResponse:
    """
    Get the CSRF token.

    Args:
        request (HttpRequest): The request.

    Returns:
        GeneralResponse: The response object
    """
    response = get_token(request)
    return response
