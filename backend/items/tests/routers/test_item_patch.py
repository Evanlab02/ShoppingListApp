"""Test the item patch endpoint."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase


class ItemPatchRouterTestCase(BaseRouterTestCase):
    """Test the item patch endpoint."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.item = ItemFactory.create(user=self.user)
        self.url = reverse("ninja-api:item_patch", kwargs={"item_id": self.item.id})

    def test_item_patch(self) -> None:
        """Test the item patch endpoint."""
        response = self.client.patch(
            self.url,
            {"name": "New Name"},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "New Name")

    def test_item_patch_not_found(self) -> None:
        """Test the item patch endpoint with a non-existent item."""
        response = self.client.patch(
            reverse("ninja-api:item_patch", kwargs={"item_id": 999999}),
            {"name": "New Name"},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_item_patch_with_no_token(self) -> None:
        """Test the item patch endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.patch(
            self.url,
            {"name": "New Name"},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
