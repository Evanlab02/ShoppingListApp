"""Tests for the view user service."""

import asyncio

from django.contrib.auth.models import AnonymousUser, User
from django.test import AsyncRequestFactory, TestCase

from authentication.errors.exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.services.views.user_service import UserService
from authentication.tests.factory import UserFactory
from authentication.tests.mocks.user_repo import MockUserRepo


class TestUserService(TestCase):
    """Tests for the view user service."""

    def setUp(self) -> None:
        """Set up the test."""
        self.service = UserService()
        self.user = UserFactory.create()

        self.request = AsyncRequestFactory()
        self.request.auser = lambda: asyncio.to_thread(lambda: AnonymousUser())  # type: ignore
        self.request.GET = {}  # type: ignore
        self.request.POST = {}  # type: ignore

        self.auth_request = AsyncRequestFactory()
        self.auth_request.auser = lambda: asyncio.to_thread(lambda: self.user)  # type: ignore
        self.auth_request.GET = {}  # type: ignore
        self.auth_request.POST = {}  # type: ignore
        return super().setUp()

    def assign_get_params(self, request: AsyncRequestFactory, params: dict[str, str]) -> None:
        """Assign the get params to the request."""
        request.GET = params  # type: ignore

    def assign_post_params(self, request: AsyncRequestFactory, params: dict[str, str]) -> None:
        """Assign the post params to the request."""
        request.POST = params  # type: ignore

    async def test_login(self) -> None:
        """Test the login function."""
        self.assign_post_params(self.request, {"username": self.user.username, "password": "test"})
        mock_service = UserService(MockUserRepo())
        await mock_service.login(self.request)  # type: ignore
        self.assertEqual(self.request.user, self.user)  # type: ignore

    async def test_login_with_user_already_logged_in(self) -> None:
        """Test the login function with a user already logged in."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.login(self.auth_request)  # type: ignore

    async def test_login_with_invalid_credentials(self) -> None:
        """Test the login function with invalid credentials."""
        self.assign_post_params(
            self.request, {"username": self.user.username, "password": "invalid"}
        )
        with self.assertRaises(InvalidCredentials):
            await self.service.login(self.request)  # type: ignore

    async def test_logout(self) -> None:
        """Test the logout function."""
        mock_service = UserService(MockUserRepo())
        await mock_service.logout(self.auth_request)  # type: ignore
        self.assertEqual(self.auth_request.user, AnonymousUser())  # type: ignore

    async def test_logout_with_user_not_logged_in(self) -> None:
        """Test the logout function with a user not logged in."""
        with self.assertRaises(UserNotLoggedIn):
            await self.service.logout(self.request)  # type: ignore

    async def test_register_user(self) -> None:
        """Test the register user function."""
        self.assign_post_params(
            self.request,
            {
                "username": "new_user",
                "password": "test",
                "password_confirm": "test",
                "first_name": "new_user",
                "last_name": "new_user",
                "email": "new_user@example.com",
            },
        )

        await self.service.register_user(self.request)  # type: ignore
        self.assertTrue(await User.objects.filter(username="new_user").aexists())

        user = await User.objects.aget(username="new_user")
        self.assertEqual(user.first_name, "new_user")
        self.assertEqual(user.last_name, "new_user")
        self.assertEqual(user.email, "new_user@example.com")

    async def test_register_user_with_logged_in_user(self) -> None:
        """Test the register user function with a logged in user."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.register_user(self.auth_request)  # type: ignore

    async def test_register_user_with_invalid_user_details(self) -> None:
        """Test the register user function with invalid user details."""
        self.assign_post_params(self.request, {"username": self.user.username, "password": "test"})
        with self.assertRaises(InvalidUserDetails):
            await self.service.register_user(self.request)  # type: ignore

    async def test_register_user_with_existing_username(self) -> None:
        """Test the register user function with an existing username."""
        self.assign_post_params(
            self.request,
            {
                "username": self.user.username,
                "password": "test",
                "password_confirm": "test",
                "first_name": "new_user",
                "last_name": "new_user",
                "email": "new_user@example.com",
            },
        )

        with self.assertRaises(UsernameAlreadyExists):
            await self.service.register_user(self.request)  # type: ignore

    async def test_register_user_with_existing_email(self) -> None:
        """Test the register user function with an existing email."""
        self.assign_post_params(
            self.request,
            {
                "username": "new_user",
                "password": "test",
                "password_confirm": "test",
                "first_name": "new_user",
                "last_name": "new_user",
                "email": self.user.email,
            },
        )

        with self.assertRaises(EmailAlreadyExists):
            await self.service.register_user(self.request)  # type: ignore

    async def test_register_user_with_non_matching_passwords(self) -> None:
        """Test the register user function with non matching passwords."""
        self.assign_post_params(
            self.request,
            {
                "username": "new_user",
                "password": "test",
                "password_confirm": "invalid",
                "first_name": "new_user",
                "last_name": "new_user",
                "email": "new_user@example.com",
            },
        )

        with self.assertRaises(NonMatchingCredentials):
            await self.service.register_user(self.request)  # type: ignore
