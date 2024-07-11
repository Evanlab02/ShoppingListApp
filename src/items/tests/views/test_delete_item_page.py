"""Contains tests for the item delete view."""

from django.test import Client

from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestItemDeleteView(BaseTestCase):
    """Contain tests for the item delete view."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test."""
        self.client.logout()
        return super().tearDown()

    def test_delete_action_invalid_method(self) -> None:
        """Test the delete action view with an invalid method."""
        response = self.client.get("/items/delete/action")
        self.assertEqual(response.status_code, 405)

    def test_delete_action_with_invalid_user(self) -> None:
        """Test the delete action view with an invalid user."""
        self.client.logout()
        response = self.client.post("/items/delete/action")
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_delete_action_with_item_that_does_not_exist(self) -> None:
        """Test the delete action view with an item that does not exist."""
        response = self.client.post("/items/delete/action", {"item-id": "9999"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Could not find item with ID: 9999.")

    def test_delete_action_with_invalid_item_id(self) -> None:
        """Test the delete action view with an invalid item id."""
        response = self.client.post("/items/delete/action", {"item-id": "badly-formatted-id"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content, b"Could not format input for item deletion, please try again."
        )

    def test_delete_action_with_empty_payload(self) -> None:
        """Test the delete action view with an empty payload."""
        response = self.client.post("/items/delete/action")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Could not find ID for deletion, please try again.")

    def test_delete_action_on_valid_item(self) -> None:
        """Test the delete action view on a valid item."""
        response = self.client.post("/items/delete/action", {"item-id": self.item.id})
        self.assertRedirects(response, "/items/me", 302, 200)

    def test_get_delete_page_invalid_method(self) -> None:
        """Test the delete page view with an invalid method."""
        response = self.client.post("/items/delete/1")
        self.assertEqual(response.status_code, 405)

    def test_get_delete_page_with_invalid_user(self) -> None:
        """Test the delete page view with an invalid user."""
        self.client.logout()
        response = self.client.get("/items/delete/1")
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_get_delete_page_for_item_that_does_not_exist(self) -> None:
        """Test the delete page view for an item that does not exist."""
        response = self.client.get("/items/delete/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Item does not exist.")

    def test_get_delete_page(self) -> None:
        """Test the delete page view."""
        response = self.client.get(f"/items/delete/{self.item.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/delete.html")
