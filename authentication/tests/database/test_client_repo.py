"""Contains tests for the client repository."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from authentication.database.client_repository import generate_token, get_client_by_user
from authentication.models import Client

from ..helpers import create_test_user, create_test_user_client


class TestClientRepository(TestCase):
    """Test the Client Repository class."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.user_client = create_test_user_client(self.user)
        return super().setUp()

    async def test_get_client_by_user(self) -> None:
        """Test getting a client by user."""
        user = self.user
        client = await get_client_by_user(user)
        self.assertEqual(client, self.user_client)

    async def test_get_client_by_user_id(self) -> None:
        """Test getting a client by user."""
        user_id = self.user.id
        client = await get_client_by_user(user_id)
        self.assertEqual(client, self.user_client)

    async def test_get_client_by_user_not_found(self) -> None:
        """Test getting a client by user when the client does not exist."""
        user_id = 999999
        with self.assertRaises(Client.DoesNotExist):
            await get_client_by_user(user_id)

    async def test_generate_token(self) -> None:
        """Test generating a token."""
        user = self.user
        token = await generate_token(user)
        await self.user_client.arefresh_from_db()

        self.assertNotEqual(token, "")
        self.assertNotEqual(self.user_client.token, "")
        self.assertEqual(token, self.user_client.token)
        self.assertIsNotNone(self.user_client.token_expiration)
        if self.user_client.token_expiration:
            self.assertGreater(self.user_client.token_expiration, timezone.now())

    async def test_generate_token_for_new_user(self) -> None:
        """Test generating a token for a new user."""
        user = await User.objects.acreate(
            username="test_user_2",
            email="test2@user.com",
            first_name="Test",
            last_name="User",
            password="test_password_2",
        )
        await user.asave()

        token = await generate_token(user)
        client = await get_client_by_user(user)

        self.assertNotEqual(token, "")
        self.assertNotEqual(client.token, "")
        self.assertEqual(token, client.token)
        self.assertIsNotNone(client.token_expiration)
        if client.token_expiration:
            self.assertGreater(client.token_expiration, timezone.now())
