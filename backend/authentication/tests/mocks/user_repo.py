"""Contains the mock user repository for testing."""

import asyncio

from django.contrib.auth.models import AnonymousUser, User
from django.http import HttpRequest

from authentication.database.user_repo import UserRepository


class MockUserRepo(UserRepository):
    """Mock user repository."""

    def __init__(self) -> None:
        """Initialize the mock user repository."""
        super().__init__()

    async def login_user(self, request: HttpRequest, user: User) -> None:
        """Login the user."""
        request.user = user
        request.auser = lambda: asyncio.to_thread(lambda: user)

    async def logout_user(self, request: HttpRequest) -> None:
        """Logout the user."""
        request.user = AnonymousUser()
        request.auser = lambda: asyncio.to_thread(lambda: AnonymousUser())
