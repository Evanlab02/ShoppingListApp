"""Contains tests for the database module."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.schemas.contexts import BaseContext, TokenContext
from authentication.services.views.client_service import disable_client, enable_client
from authentication.tests.helpers import create_test_user


class TestClientRepository(TestCase):
    """Test the ClientRepository class."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.client = Client()
        self.client.force_login(self.user)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    async def test_enable_client(self) -> None:
        """Test enabling a client."""
        context = await enable_client(self.user)
        self.assertIsNotNone(context)
        self.assertIsInstance(context, TokenContext)
        self.assertIsNotNone(context.token)
        self.assertIsInstance(context.token, str)
        self.assertIsNone(context.error)

    async def test_enable_client_already_exists(self) -> None:
        """Test enabling a client when one already exists."""
        await enable_client(self.user)
        context = await enable_client(self.user)
        self.assertIsNotNone(context)
        self.assertIsInstance(context, TokenContext)
        self.assertIsNone(context.token)
        self.assertIsNotNone(context.error)
        self.assertIsInstance(context.error, str)
        self.assertEqual(context.error, "Client already registered.")

    async def test_disable_client(self) -> None:
        """Test disabling a client."""
        await enable_client(self.user)
        context = await disable_client(self.user)
        self.assertIsNotNone(context)
        self.assertIsInstance(context, BaseContext)
        self.assertIsNone(context.error)

    async def test_disable_client_does_not_exist(self) -> None:
        """Test disabling a client that does not exist."""
        context = await disable_client(self.user)
        self.assertIsNotNone(context)
        self.assertIsInstance(context, BaseContext)
        self.assertIsNotNone(context.error)
        self.assertIsInstance(context.error, str)
        self.assertEqual(context.error, "Client does not exist.")
