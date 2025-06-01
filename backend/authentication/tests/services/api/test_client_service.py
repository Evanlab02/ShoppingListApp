"""Test the API client service."""

import jwt
from django.test import TestCase

from authentication.services.api.client_service import ClientService
from authentication.tests.factory import ClientFactory, UserFactory


class TestClientService(TestCase):
    """Test the client service."""

    def setUp(self) -> None:
        """Set up the test."""
        self.service = ClientService()
        self.user = UserFactory.create()
        self.api_client = ClientFactory.create(user=self.user)
        return super().setUp()

    async def test_get_token(self) -> None:
        """Test the get token function."""
        token, secret = await self.service.get_token(self.user)
        self.assertIsNotNone(token)
        self.assertIsNotNone(secret)

    async def test_get_token_decodes_correctly(self) -> None:
        """Test the get token function."""
        token, secret = await self.service.get_token(self.user)
        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded_token["username"], self.user.username)
        self.assertEqual(decoded_token["client_id"], self.api_client.id)
