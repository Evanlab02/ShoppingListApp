"""Contains the tests for the item delete endpoint."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase


class ItemDeleteRouterTestCase(BaseRouterTestCase):
    """Test the item delete endpoint."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.item = ItemFactory.create(user=self.user)
        self.url = reverse("ninja-api:item_delete", kwargs={"item_id": self.item.id})

    def test_item_delete(self) -> None:
        """Test the item delete endpoint."""
        response = self.client.delete(
            self.url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Deleted Item.")

    def test_item_delete_not_found(self) -> None:
        """Test the item delete endpoint with a non-existent item."""
        response = self.client.delete(
            reverse("ninja-api:item_delete", kwargs={"item_id": 999999}),
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_item_delete_with_no_token(self) -> None:
        """Test the item delete endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.delete(
            self.url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
