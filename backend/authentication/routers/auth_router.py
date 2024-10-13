"""Contains authentication routes."""

import logging

from django.http import HttpRequest
from ninja import Router

from authentication.schemas.input import NewUser, UserCredentials
from authentication.schemas.output import GeneralResponse
from authentication.services.api.user_service import login, logout, register_user

log = logging.getLogger(__name__)
log.info("Loading authentication router...")
auth_router = Router(tags=["Authentication"])


@auth_router.post("/login", response={200: GeneralResponse})
async def login_user(request: HttpRequest, user_creds: UserCredentials) -> GeneralResponse:
    """
    Login a user.

    Args:
        request (HttpRequest): The request object
        user_details (UserCredentials): The user credentials

    Returns:
        GeneralResponse: The response object
    """
    log.info(f"Retrieved request to log user in. ({user_creds.username})")
    response = await login(request, user_creds.username, user_creds.password)
    return response


@auth_router.post("/logout", response={200: GeneralResponse})
async def logout_user(request: HttpRequest) -> GeneralResponse:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request object

    Returns:
        GeneralResponse: The response object
    """
    log.info("Retrieved request to log user out.")
    response = await logout(request)
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
    log.info("Retrieved request to register user.")
    user = await request.auser()
    response = await register_user(user, new_user)
    return response


log.info("Loaded authentication router.")
