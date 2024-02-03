"""Contains the tests for the api user service of the authentication app."""

from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase

from authentication.errors.api_exceptions import (
    EmailAlreadyExists,
    InvalidUserDetails,
    NonMatchingCredentials,
    UserAlreadyLoggedIn,
    UsernameAlreadyExists,
)
from authentication.schemas.input import NewUser
from authentication.services.api.user_service import register_user


class TestApiUserService(TestCase):
    """Test the api user service."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        return super().setUp()

    async def test_register_user(self) -> None:
        """Test the register user function."""
        user = AnonymousUser()
        new_user = NewUser(
            username="registeruser",
            password="test",
            password_confirmation="test",
            first_name="test",
            last_name="test",
            email="registertest@user.com",
        )
        response = await register_user(user, new_user)
        self.assertEqual(response.message, "User successfully registered.")
        self.assertEqual(response.detail, "")

    async def test_register_user_when_already_logged_in(self) -> None:
        """Test the register user function."""
        user = await User.objects.acreate(
            username="loggedinuser",
            password="test",
            email="loggedinuser@gmail.com",
            first_name="loggedin",
            last_name="user",
        )
        await user.asave()

        new_user = NewUser(
            username="existinguser",
            password="test",
            password_confirmation="test",
            first_name="test",
            last_name="test",
            email="test@gmail.com",
        )

        with self.assertRaises(UserAlreadyLoggedIn):
            await register_user(user, new_user)

    async def test_register_user_with_empty_detail(self) -> None:
        """Test the register user function."""
        user = AnonymousUser()

        new_user = NewUser(
            username="",
            password="test",
            password_confirmation="test",
            first_name="",
            last_name="",
            email="test@user.com",
        )

        with self.assertRaises(InvalidUserDetails):
            await register_user(user, new_user)

    async def test_register_user_with_existing_username(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()
        user = await User.objects.acreate(
            username="existinguser",
            password="test",
            email="existinguser@gmail.com",
            first_name="existing",
            last_name="user",
        )
        await user.asave()

        new_user = NewUser(
            username="existinguser",
            password="test",
            password_confirmation="test",
            first_name="test",
            last_name="test",
            email="test@gmail.com",
        )

        with self.assertRaises(UsernameAlreadyExists):
            await register_user(api_user, new_user)

    async def test_register_user_with_existing_email(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()
        user = await User.objects.acreate(
            username="existingemail",
            password="test",
            email="existingemail@gmail.com",
            first_name="existing",
            last_name="email",
        )
        await user.asave()

        new_user = NewUser(
            username="testuser",
            password="test",
            password_confirmation="test",
            first_name="test",
            last_name="test",
            email="existingemail@gmail.com",
        )

        with self.assertRaises(EmailAlreadyExists):
            await register_user(api_user, new_user)

    async def test_register_user_with_non_matching_passwords(self) -> None:
        """Test the register user function."""
        api_user = AnonymousUser()

        new_user = NewUser(
            username="testuser",
            password="test",
            password_confirmation="test1",
            first_name="test",
            last_name="test",
            email="non_matchingpass@gmail.com",
        )

        with self.assertRaises(NonMatchingCredentials):
            await register_user(api_user, new_user)
