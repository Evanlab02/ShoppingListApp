"""Contains the tests for token authentication."""

import pytest
from django.test import AsyncRequestFactory, TestCase

from authentication.auth.token_auth import TokenAuth
from authentication.tests.factory import ClientFactory, UserFactory


class TestTokenAuth(TestCase):
    """Test the token authentication class."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory()
        self.client = ClientFactory(user=self.user)
        self.token_auth = TokenAuth()
        self.factory = AsyncRequestFactory()

        self.request = self.factory.get("/")
        self.request.headers = {"X-API-Token": self.client.token}

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    async def test_authenticate_with_valid_token(self):
        """Test the authenticate method with a valid token."""
        result = await self.token_auth.__call__(self.request)
        self.assertEqual(result, self.client)

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    async def test_authenticate_with_invalid_token(self):
        """Test the authenticate method with an invalid token."""
        self.request.headers = {"X-API-Token": "invalid"}
        result = await self.token_auth.__call__(self.request)
        self.assertIsNone(result)

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    async def test_authenticate_with_no_token(self):
        """Test the authenticate method with no token."""
        self.request.headers = {}
        result = await self.token_auth.__call__(self.request)
        self.assertIsNone(result)
