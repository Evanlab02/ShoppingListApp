"""Contains tests for the delete endpoint in the item router."""

from asgiref.sync import async_to_sync
from django.test import Client

from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestDeleteEndpoint(BaseTestCase):
    """Test the delete endpoint in the item router."""

    def setUp(self) -> None:
        """Set up the tests."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the tests."""
        return super().tearDown()

    def test_delete_item(self) -> None:
        """Test that the item is deleted."""
        response = self.client.delete(f"/api/v1/items/delete/{self.item.id}")
        self.assertEqual(response.status_code, 200)

        item_exists = Item.objects.filter(id=self.item.id).exists()
        self.assertFalse(item_exists)

        response_body = response.json()
        self.assertEqual(response_body["message"], "Deleted Item.")
        self.assertEqual(response_body["detail"], f"Item with ID #{self.item.id} was deleted.")

    def test_delete_item_invalid_id(self) -> None:
        """Test deleting an item with an invalid id."""
        response = self.client.delete("/api/v1/items/delete/999999")
        self.assertEqual(response.status_code, 404)

        # Check item still exists
        item_exists = Item.objects.filter(id=self.item.id).exists()
        self.assertTrue(item_exists)

        response_body = response.json()
        self.assertEqual(response_body["detail"], "Item with id '999999' does not exist.")

    def test_delete_item_invalid_user(self) -> None:
        """Test deleting an item that does not belong to that user."""
        user = async_to_sync(self.create_temporary_user)()
        self.client.logout()

        self.client.force_login(user)
        response = self.client.delete(f"/api/v1/items/delete/{self.item.id}")
        self.assertEqual(response.status_code, 404)

        # Check item still exists
        item_exists = Item.objects.filter(id=self.item.id).exists()
        self.assertTrue(item_exists)

        response_body = response.json()
        self.assertEqual(response_body["detail"], f"Item with id '{self.item.id}' does not exist.")

    def test_delete_item_invalid_method(self) -> None:
        """Test deleting an item with an invalid method."""
        response = self.client.get(f"/api/v1/items/delete/{self.item.id}")
        self.assertEqual(response.status_code, 405)

        # Check item still exists
        item_exists = Item.objects.filter(id=self.item.id).exists()
        self.assertTrue(item_exists)
