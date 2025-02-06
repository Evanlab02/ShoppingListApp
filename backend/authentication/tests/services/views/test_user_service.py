"""Tests for the view user service."""

import asyncio

from django.contrib.auth.models import AnonymousUser, User
from django.test import AsyncRequestFactory, TestCase

from authentication.errors.api_exceptions import (
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
        self.user = UserFactory()

        self.request = AsyncRequestFactory()
        self.request.auser = lambda: asyncio.to_thread(lambda: AnonymousUser())
        self.request.GET = {}
        self.request.POST = {}

        self.auth_request = AsyncRequestFactory()
        self.auth_request.auser = lambda: asyncio.to_thread(lambda: self.user)
        self.auth_request.GET = {}
        self.auth_request.POST = {}
        return super().setUp()

    def assign_get_params(self, request: AsyncRequestFactory, params: dict[str, str]) -> None:
        """Assign the get params to the request."""
        request.GET = params

    def assign_post_params(self, request: AsyncRequestFactory, params: dict[str, str]) -> None:
        """Assign the post params to the request."""
        request.POST = params

    async def test_get_login_view_context(self) -> None:
        """Test the get login view context function."""
        context = await self.service.get_login_view_context(self.request)
        self.assertEqual(context.error, None)
        self.assertEqual(context.username_input, "username")
        self.assertEqual(context.password_input, "password")
        self.assertEqual(context.submit_login, "submit")

    async def test_get_login_view_context_with_error(self) -> None:
        """Test the get login view context function with an error."""
        self.assign_get_params(self.request, {"error": "test_error"})
        context = await self.service.get_login_view_context(self.request)
        self.assertEqual(context.error, "test_error")

    async def test_get_login_view_context_with_user_already_logged_in(self) -> None:
        """Test the get login view context function with a user already logged in."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.get_login_view_context(self.auth_request)

    async def test_get_logout_view_context(self) -> None:
        """Test the get logout view context function."""
        context = await self.service.get_logout_view_context(self.auth_request)
        self.assertEqual(context.error, None)
        self.assertEqual(context.submit_logout, "submit")
        self.assertEqual(context.submit_cancel, "cancel")

    async def test_get_logout_view_context_with_error(self) -> None:
        """Test the get logout view context function with a user not logged in."""
        self.assign_get_params(self.auth_request, {"error": "test_error"})
        context = await self.service.get_logout_view_context(self.auth_request)
        self.assertEqual(context.error, "test_error")

    async def test_get_logout_view_context_with_user_not_logged_in(self) -> None:
        """Test the get logout view context function with a user already logged in."""
        with self.assertRaises(UserNotLoggedIn):
            await self.service.get_logout_view_context(self.request)

    async def test_get_register_page_context(self) -> None:
        """Test the get register page context function."""
        context = await self.service.get_register_page_context(self.request)
        self.assertIsNotNone(context)
        self.assertEqual(context.error, None)
        self.assertEqual(context.username_input, "username")
        self.assertEqual(context.email_input, "email")
        self.assertEqual(context.first_name_input, "first_name")
        self.assertEqual(context.last_name_input, "last_name")
        self.assertEqual(context.password_input, "password")
        self.assertEqual(context.password_confirm_input, "password_confirm")
        self.assertEqual(context.submit_register, "submit")

    async def test_get_register_page_context_with_error(self) -> None:
        """Test the get register page context function with an error."""
        self.assign_get_params(self.request, {"error": "test_error"})
        context = await self.service.get_register_page_context(self.request)
        self.assertEqual(context.error, "test_error")

    async def test_get_register_page_context_with_user_already_logged_in(self) -> None:
        """Test the get register page context function with a user already logged in."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.get_register_page_context(self.auth_request)

    async def test_login(self) -> None:
        """Test the login function."""
        self.assign_post_params(self.request, {"username": self.user.username, "password": "test"})
        mock_service = UserService(MockUserRepo())
        await mock_service.login(self.request)
        self.assertEqual(self.request.user, self.user)

    async def test_login_with_user_already_logged_in(self) -> None:
        """Test the login function with a user already logged in."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.login(self.auth_request)

    async def test_login_with_invalid_credentials(self) -> None:
        """Test the login function with invalid credentials."""
        self.assign_post_params(
            self.request, {"username": self.user.username, "password": "invalid"}
        )
        with self.assertRaises(InvalidCredentials):
            await self.service.login(self.request)

    async def test_logout(self) -> None:
        """Test the logout function."""
        mock_service = UserService(MockUserRepo())
        await mock_service.logout(self.auth_request)
        self.assertEqual(self.auth_request.user, AnonymousUser())

    async def test_logout_with_user_not_logged_in(self) -> None:
        """Test the logout function with a user not logged in."""
        with self.assertRaises(UserNotLoggedIn):
            await self.service.logout(self.request)

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

        await self.service.register_user(self.request)
        self.assertTrue(await User.objects.filter(username="new_user").aexists())

        user = await User.objects.aget(username="new_user")
        self.assertEqual(user.first_name, "new_user")
        self.assertEqual(user.last_name, "new_user")
        self.assertEqual(user.email, "new_user@example.com")

    async def test_register_user_with_logged_in_user(self) -> None:
        """Test the register user function with a logged in user."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.register_user(self.auth_request)

    async def test_register_user_with_invalid_user_details(self) -> None:
        """Test the register user function with invalid user details."""
        self.assign_post_params(self.request, {"username": self.user.username, "password": "test"})
        with self.assertRaises(InvalidUserDetails):
            await self.service.register_user(self.request)

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
            await self.service.register_user(self.request)

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
            await self.service.register_user(self.request)

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
            await self.service.register_user(self.request)
