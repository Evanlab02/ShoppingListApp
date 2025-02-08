"""Tests for the ClientRepository class."""

import jwt
from django.test import TestCase

from authentication.database.client_repo import ClientRepository
from authentication.tests.factory import ClientFactory, UserFactory


class TestClientRepository(TestCase):
    """Tests for the ClientRepository class."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.api_client = ClientFactory.create(user=self.user)
        self.repo = ClientRepository()

    async def test_get_token(self) -> None:
        """Test the get_token method."""
        self.assertEqual(self.api_client.client_secret, "")
        self.assertEqual(self.api_client.token, "")
        self.assertEqual(self.api_client.token_expiration, 0)

        token, secret = await self.repo.get_token(self.user)

        await self.api_client.arefresh_from_db()
        self.assertIsNotNone(token)
        self.assertIsNotNone(secret)
        self.assertIsNotNone(self.api_client.client_secret)
        self.assertIsNotNone(self.api_client.token)
        self.assertIsNotNone(self.api_client.token_expiration)

    async def test_client_get_token_decodes_correctly(self) -> None:
        """Test that the get_token method decodes correctly."""
        token, secret = await self.repo.get_token(self.user)
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded["username"], self.user.username)
        self.assertEqual(decoded["client_id"], self.api_client.id)
