"""Contains authentication routes."""

import logging

from django.http import HttpRequest
from ninja import Router

from authentication.schemas.input import NewUser, UserCredentials
from authentication.schemas.output import GeneralResponse
from authentication.services.api.user_service import UserService
from shoppingapp.schemas.shared import ErrorSchema

log = logging.getLogger(__name__)
auth_router = Router(tags=["Authentication"])
service = UserService()


@auth_router.post(
    "/login",
    response={200: GeneralResponse, 400: ErrorSchema, 500: ErrorSchema},
    url_name="auth_login",
)
async def login_user(
    request: HttpRequest, user_creds: UserCredentials
) -> GeneralResponse | ErrorSchema:
    """
    Login a user.

    Args:
        request (HttpRequest): The request object
        user_details (UserCredentials): The user credentials

    Returns:
        GeneralResponse: The response object
    """
    return await service.login(request, user_creds.username, user_creds.password)


@auth_router.post(
    "/logout",
    response={200: GeneralResponse, 400: ErrorSchema, 500: ErrorSchema},
    url_name="auth_logout",
)
async def logout_user(request: HttpRequest) -> GeneralResponse | ErrorSchema:
    """
    Logout a user.

    Args:
        request (HttpRequest): The request object

    Returns:
        GeneralResponse: The response object
    """
    return await service.logout(request)


@auth_router.post(
    "/register",
    response={201: GeneralResponse, 400: ErrorSchema, 500: ErrorSchema},
    url_name="auth_register",
)
async def register(request: HttpRequest, new_user: NewUser) -> GeneralResponse | ErrorSchema:
    """
    Register a new user.

    Args:
        request (HttpRequest): The request object
        new_user (NewUser): The new user data

    Returns:
        GeneralResponse: The response object
    """
    user = await request.auser()
    return await service.register_user(user, new_user)
