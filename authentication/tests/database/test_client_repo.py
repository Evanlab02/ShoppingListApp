"""Contains tests for the client repository."""

import pytest
from django.test import TestCase

from authentication.database.client_repository import get_client_by_user_id
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
        user_id = self.user.id
        client = await get_client_by_user_id(user_id)
        self.assertEqual(client, self.user_client)

    async def test_get_client_by_user_not_found(self) -> None:
        """Test getting a client by user when the client does not exist."""
        user_id = 999999
        with self.assertRaises(Client.DoesNotExist):
            await get_client_by_user_id(user_id)
