"""Contains tests for the database module."""

from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase

from authentication.database.user_repo import UserRepository
from authentication.tests.factory import UserFactory


class TestUserRepository(TestCase):
    """Test the UserRepository class."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        self.repo = UserRepository()
        self.user = UserFactory()  # type: ignore
        return super().setUp()

    async def test_create_user(self) -> None:
        """Test the create_user method."""
        username = "testcreate"
        password = "testcreate"
        email = "test@gmail.com"
        first_name = "test"
        last_name = "create"

        user = await self.repo.create_user(username, password, first_name, last_name, email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_user_is_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        self.client.force_login(self.user)
        is_authenticated = self.repo.is_user_authenticated(self.user)
        self.assertTrue(is_authenticated)

    def test_user_is_not_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        user = AnonymousUser()
        is_authenticated = self.repo.is_user_authenticated(user)
        self.assertFalse(is_authenticated)

    async def test_username_exists(self) -> None:
        """Test the does_username_exist method."""
        username_exists = await self.repo.does_username_exist(self.user.username)
        self.assertTrue(username_exists)

    async def test_username_does_not_exist(self) -> None:
        """Test the does_username_exist method."""
        username_exists = await self.repo.does_username_exist("thisshouldnotexist")
        self.assertFalse(username_exists)

    async def test_email_exists(self) -> None:
        """Test the does_email_exist method."""
        email_exists = await self.repo.does_email_exist(self.user.email)
        self.assertTrue(email_exists)

    async def test_email_does_not_exist(self) -> None:
        """Test the does_email_exist method."""
        email_exists = await self.repo.does_email_exist("thisshouldnotexist@gmail.com")
        self.assertFalse(email_exists)
