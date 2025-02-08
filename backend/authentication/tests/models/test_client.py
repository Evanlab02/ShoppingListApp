"""Tests for the ApiClient model."""

import jwt
from django.test import TestCase

from authentication.tests.factory import ClientFactory


class TestClient(TestCase):
    """Tests for the ApiClient model."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.api_client = ClientFactory.create()

    def test_client_str(self) -> None:
        """Test the __str__ method."""
        self.assertEqual(str(self.api_client), f"ApiClient for {self.api_client.user.username}")

    async def test_client_get_token(self) -> None:
        """Test the get_token method."""
        self.assertIsNone(self.api_client.client_secret)
        self.assertIsNone(self.api_client.token)
        self.assertEqual(self.api_client.token_expiration, 0)

        token, secret = await self.api_client.get_token(self.api_client.user)

        await self.api_client.arefresh_from_db()
        self.assertIsNotNone(token)
        self.assertIsNotNone(secret)
        self.assertIsNotNone(self.api_client.client_secret)
        self.assertIsNotNone(self.api_client.token)
        self.assertIsNotNone(self.api_client.token_expiration)

    async def test_client_get_token_decodes_correctly(self) -> None:
        """Test that the get_token method decodes correctly."""
        token, secret = await self.api_client.get_token(self.api_client.user)
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded["username"], self.api_client.user.username)
        self.assertEqual(decoded["client_id"], self.api_client.id)
