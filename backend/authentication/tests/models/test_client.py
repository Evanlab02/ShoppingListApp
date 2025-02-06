"""Tests for the ApiClient model."""

import jwt
from django.test import TestCase

from authentication.tests.factory import ClientFactory


class TestClient(TestCase):
    """Tests for the ApiClient model."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = ClientFactory()

    def test_client_str(self) -> None:
        """Test the __str__ method."""
        self.assertEqual(str(self.client), f"ApiClient for {self.client.user.username}")

    async def test_client_get_token(self) -> None:
        """Test the get_token method."""
        self.assertIsNone(self.client.client_secret)
        self.assertIsNone(self.client.token)
        self.assertEqual(self.client.token_expiration, 0)

        token, secret = await self.client.get_token(self.client.user)

        await self.client.arefresh_from_db()
        self.assertIsNotNone(token)
        self.assertIsNotNone(secret)
        self.assertIsNotNone(self.client.client_secret)
        self.assertIsNotNone(self.client.token)
        self.assertIsNotNone(self.client.token_expiration)

    async def test_client_get_token_decodes_correctly(self) -> None:
        """Test that the get_token method decodes correctly."""
        token, secret = await self.client.get_token(self.client.user)
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded["username"], self.client.user.username)
        self.assertEqual(decoded["client_id"], self.client.id)
