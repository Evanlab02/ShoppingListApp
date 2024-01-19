"""Contains tests for the database module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.database.client_repository import enable_for_user
from authentication.errors.api_exceptions import ApiClientAlreadyRegistered

from ..helpers import create_test_user


class TestUserRepository(TestCase):
    """Test the UserRepository class."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.client = Client()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    async def test_enable_client(self) -> None:
        """Test enabling a client."""
        client_secret = await enable_for_user(self.user)
        self.assertIsNotNone(client_secret)
        self.assertIsInstance(client_secret, str)

    async def test_enable_client_already_exists(self) -> None:
        """Test enabling a client when one already exists."""
        await enable_for_user(self.user)
        with self.assertRaises(ApiClientAlreadyRegistered):
            await enable_for_user(self.user)
