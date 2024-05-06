"""Contains tests for the item router update function."""

from asgiref.sync import async_to_sync
from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestUpdateRouter(BaseTestCase):
    """Test the item router update functions."""

    def setUp(self) -> None:
        """Set up the tests."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_update_item_no_changes(self) -> None:
        """Test that the item is updated with no changes."""
        response = self.client.patch(
            f"/api/v1/items/update/{self.item.id}", {}, content_type="application/json"
        )
        item = response.json()
        self.assertEqual(item["name"], "Test Item")
        self.assertEqual(item["price"], "100.00")
        self.assertEqual(item["description"], "Test Description")

        self.assertEqual(item["store"]["name"], "Base Test Store")
        self.assertEqual(item["user"]["username"], self.user.username)

    def test_update_item_with_changes(self) -> None:
        """Test that the item is updated with changes."""
        temp_store = async_to_sync(self.create_temporary_store)()
        response = self.client.patch(
            f"/api/v1/items/update/{self.item.id}",
            {
                "store_id": temp_store.id,
                "name": "Updated Item",
                "price": "200.00",
                "description": "Updated Description",
            },
            content_type="application/json",
        )
        item = response.json()
        self.assertEqual(item["name"], "Updated Item")
        self.assertEqual(item["price"], "200.0")
        self.assertEqual(item["description"], "Updated Description")

        self.assertEqual(item["store"]["name"], "Temporary Store")
        self.assertEqual(item["user"]["username"], self.user.username)
