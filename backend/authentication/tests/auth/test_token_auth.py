"""Contains the tests for token authentication."""

from django.test import AsyncRequestFactory, TestCase

from authentication.auth.token_auth import TokenAuth
from authentication.tests.factory import ClientFactory, UserFactory


class TestTokenAuth(TestCase):
    """Test the token authentication class."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.api_client = ClientFactory.create(user=self.user)
        self.token_auth = TokenAuth()
        self.factory = AsyncRequestFactory()

        self.request = self.factory.get("/")
        self.request.headers = {"X-API-Token": self.api_client.token}  # type: ignore

    async def test_authenticate_with_valid_token(self) -> None:
        """Test the authenticate method with a valid token."""
        result = await self.token_auth.__call__(self.request)  # type: ignore
        self.assertEqual(result, self.api_client)

    async def test_authenticate_with_invalid_token(self) -> None:
        """Test the authenticate method with an invalid token."""
        self.request.headers = {"X-API-Token": "invalid"}  # type: ignore
        result = await self.token_auth.__call__(self.request)  # type: ignore
        self.assertIsNone(result)

    async def test_authenticate_with_no_token(self) -> None:
        """Test the authenticate method with no token."""
        self.request.headers = {}  # type: ignore
        result = await self.token_auth.__call__(self.request)  # type: ignore
        self.assertIsNone(result)
