"""Test the item detail endpoint."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase


class ItemDetailRouterTestCase(BaseRouterTestCase):
    """Test the item detail endpoint."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.item = ItemFactory.create()
        self.url = reverse("ninja-api:item_detail", kwargs={"item_id": self.item.id})

    def test_item_detail(self) -> None:
        """Test the item detail endpoint."""
        response = self.client.get(
            self.url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], self.item.id)

    def test_item_detail_not_found(self) -> None:
        """Test the item detail endpoint with a non-existent item."""
        response = self.client.get(
            reverse("ninja-api:item_detail", kwargs={"item_id": 999999}),
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_item_detail_with_no_token(self) -> None:
        """Test the item detail endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
