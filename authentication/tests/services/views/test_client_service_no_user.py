"""Contains tests for the database module."""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase

from authentication.schemas.contexts import BaseContext, TokenContext
from authentication.services.views.client_service import disable_client, enable_client


class TestClientRepository(TestCase):
    """Test the ClientRepository class."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        return super().tearDown()

    async def test_enable_client_logged_out(self) -> None:
        """Test enabling a client when the user is logged out."""
        context = await enable_client(AnonymousUser())
        self.assertIsNotNone(context)
        self.assertIsInstance(context, TokenContext)
        self.assertIsNone(context.token)
        self.assertIsNotNone(context.error)
        self.assertIsInstance(context.error, str)
        self.assertEqual(context.error, "User is not authenticated.")

    async def test_disable_client_logged_out(self) -> None:
        """Test disabling a client when the user is logged out."""
        context = await disable_client(AnonymousUser())
        self.assertIsNotNone(context)
        self.assertIsInstance(context, BaseContext)
        self.assertIsNotNone(context.error)
        self.assertIsInstance(context.error, str)
        self.assertEqual(context.error, "User is not authenticated.")
