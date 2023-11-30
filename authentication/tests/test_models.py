"""Contains tests for the Client model."""

import pytest
from django.test import TestCase
from django.utils import timezone

from .helpers import create_test_user, create_test_user_client


class TestClient(TestCase):
    """Test the Client model."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.user_client = create_test_user_client(self.user)
        return super().setUp()

    def test_client(self) -> None:
        """Test the Client model."""
        self.assertEqual(self.user_client.user, self.user)
        self.assertEqual(self.user_client.token, "")
        self.assertIsNone(self.user_client.token_expiration)

    def test_client_str(self) -> None:
        """Test the client __str__ method."""
        self.assertEqual(
            str(self.user_client), f"{self.user.username} ({self.user.email})"
        )

    async def test_client_generate_token(self) -> None:
        """Test the client generate_token method."""
        await self.user_client.generate_token()
        self.assertNotEqual(self.user_client.token, "")
        self.assertIsNotNone(self.user_client.token_expiration)
        if self.user_client.token_expiration:
            self.assertGreater(self.user_client.token_expiration, timezone.now())
