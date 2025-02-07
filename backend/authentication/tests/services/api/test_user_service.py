"""Contains the tests for the api user service of the authentication app."""

import asyncio

from django.contrib.auth.models import AnonymousUser, User
from django.test import AsyncRequestFactory, Client, TestCase

from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
    UserNotLoggedIn,
)
from authentication.services.api.user_service import UserService
from authentication.tests.factory import NewUserSchemaFactory, UserFactory
from authentication.tests.mocks.user_repo import MockUserRepo


class TestApiUserService(TestCase):
    """Test the api user service."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
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

    async def test_register_user(self) -> None:
        """Test the register user function."""
        user = AnonymousUser()
        new_user = NewUserSchemaFactory()
        response = await self.service.register_user(user, new_user)
        self.assertEqual(response.message, "User successfully registered.")
        self.assertEqual(response.detail, "")

    async def test_register_user_when_already_logged_in(self) -> None:
        """Test the register user function."""
        new_user = NewUserSchemaFactory()

        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.register_user(self.user, new_user)

    async def test_register_user_with_empty_detail(self) -> None:
        """Test the register user function."""
        user = AnonymousUser()
        new_user = NewUserSchemaFactory(
            username="",
            first_name="",
            last_name="",
            email="",
        )

        with self.assertRaises(InvalidUserDetails):
            await self.service.register_user(user, new_user)

    async def test_register_user_with_existing_username(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()

        self.user.username = "existinguser"
        await self.user.asave()

        new_user = NewUserSchemaFactory(username="existinguser")

        with self.assertRaises(UsernameAlreadyExists):
            await self.service.register_user(api_user, new_user)

    async def test_register_user_with_existing_email(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()
        self.user.email = "existingemail@gmail.com"
        await self.user.asave()

        new_user = NewUserSchemaFactory(email="existingemail@gmail.com")

        with self.assertRaises(EmailAlreadyExists):
            await self.service.register_user(api_user, new_user)

    async def test_register_user_with_non_matching_passwords(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()

        new_user = NewUserSchemaFactory(password="test", password_confirmation="test1")

        with self.assertRaises(NonMatchingCredentials):
            await self.service.register_user(api_user, new_user)

    async def test_login_user(self) -> None:
        """Test the login user function."""
        mock_service = UserService(MockUserRepo())
        response = await mock_service.login(self.request, self.user.username, "test")
        self.assertEqual(response.message, "User successfully logged in.")
        self.assertEqual(response.detail, "")

    async def test_login_user_when_already_logged_in(self) -> None:
        """Test the login user function."""
        with self.assertRaises(UserAlreadyLoggedIn):
            await self.service.login(self.auth_request, self.user.username, "test")

    async def test_login_user_with_invalid_credentials(self) -> None:
        """Test the login user function."""
        with self.assertRaises(InvalidCredentials):
            await self.service.login(self.request, self.user.username, "invalid")

    async def test_logout_user(self) -> None:
        """Test the logout user function."""
        mock_service = UserService(MockUserRepo())
        response = await mock_service.logout(self.auth_request)
        self.assertEqual(response.message, "User successfully logged out.")
        self.assertEqual(response.detail, "")

    async def test_logout_user_when_not_logged_in(self) -> None:
        """Test the logout user function."""
        with self.assertRaises(UserNotLoggedIn):
            await self.service.logout(self.request)
