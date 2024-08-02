"""
URL configuration for shoppingapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import logging

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path
from ninja import NinjaAPI

from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.routers.auth_router import auth_router
from dashboard.routers.dashboard_router import dashboard_router
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.routers.item_router import item_router
from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.routers.store_router import store_router

log = logging.getLogger(__name__)
log.info("Loading urls...")

version = open("../version.txt").read().strip()
api = NinjaAPI(title="Shopping App API", version=version)
api.add_router("/auth", auth_router)
api.add_router("/stores", store_router)
api.add_router("/items", item_router)
api.add_router("/dashboard", dashboard_router)


@api.exception_handler(EmailAlreadyExists)
def email_already_exists_handler(
    request: HttpRequest, exception: EmailAlreadyExists
) -> HttpResponse:
    """Handle EmailAlreadyExists exception."""
    log.warning(f"Email already exists: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(InvalidCredentials)
def invalid_credentials_handler(
    request: HttpRequest, exception: InvalidCredentials
) -> HttpResponse:
    """Handle InvalidCredentials exception."""
    log.warning(f"Invalid Credentials: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(InvalidUserDetails)
def invalid_user_details_handler(
    request: HttpRequest, exception: InvalidUserDetails
) -> HttpResponse:
    """Handle InvalidUserDetails exception."""
    log.warning(f"Invalid User Details: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(NonMatchingCredentials)
def non_matching_credentials_handler(
    request: HttpRequest, exception: NonMatchingCredentials
) -> HttpResponse:
    """Handle NonMatchingCredentials exception."""
    log.warning(f"Credentials do not match: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(UserAlreadyLoggedIn)
def user_already_logged_in_handler(
    request: HttpRequest, exception: UserAlreadyLoggedIn
) -> HttpResponse:
    """Handle UserAlreadyLoggedIn exception."""
    log.warning(f"User already logged in: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(UsernameAlreadyExists)
def username_already_exists_handler(
    request: HttpRequest, exception: UsernameAlreadyExists
) -> HttpResponse:
    """Handle UsernameAlreadyExists exception."""
    log.warning(f"Username already exists: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(UserNotLoggedIn)
def user_not_logged_in_handler(request: HttpRequest, exception: UserNotLoggedIn) -> HttpResponse:
    """Handle UserNotLoggedIn exception."""
    log.warning(f"User not logged in: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(InvalidStoreType)
def invalid_store_type_handler(request: HttpRequest, exception: InvalidStoreType) -> HttpResponse:
    """Handle InvalidStoreType exception."""
    log.warning(f"Invalid Store Type: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(StoreAlreadyExists)
def store_already_exists_handler(
    request: HttpRequest, exception: StoreAlreadyExists
) -> HttpResponse:
    """Handle StoreAlreadyExists exception."""
    log.warning(f"Store already exists: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(StoreDoesNotExist)
def store_does_not_exist_handler(
    request: HttpRequest, exception: StoreDoesNotExist
) -> HttpResponse:
    """Handle StoreDoesNotExist exception."""
    log.warning(f"Store does not exist: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=404)


@api.exception_handler(ItemAlreadyExists)
def item_already_exists_handler(request: HttpRequest, exception: ItemAlreadyExists) -> HttpResponse:
    """Handle ItemAlreadyExists exception."""
    log.warning(f"Item already exists: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=400)


@api.exception_handler(ItemDoesNotExist)
def item_does_not_exist_handler(request: HttpRequest, exception: ItemDoesNotExist) -> HttpResponse:
    """Handle ItemDoesNotExist exception."""
    log.warning(f"Item does not exist: {exception}")
    return api.create_response(request, {"detail": str(exception)}, status=404)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
    path("", include("authentication.urls")),
    path("stores/", include("stores.urls")),
    path("items/", include("items.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

log.info("Loaded urls.")
