"""Test the item update endpoint."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class ItemUpdateRouterTestCase(BaseRouterTestCase):
    """Test the item update endpoint."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(user=self.user)
        self.url = reverse("ninja-api:item_update", kwargs={"item_id": self.item.id})

    def test_item_update(self) -> None:
        """Test the item update endpoint."""
        response = self.client.put(
            self.url,
            {
                "name": "New Name",
                "price": 9987.00,
                "description": "New Description",
                "store_id": self.store.id,
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "New Name")
        self.assertEqual(response.json()["price"], "9987.0")
        self.assertEqual(response.json()["description"], "New Description")
        self.assertEqual(response.json()["store"]["id"], self.store.id)
        self.assertEqual(response.json()["store"]["name"], self.store.name)

    def test_item_update_not_found(self) -> None:
        """Test the item update endpoint with a non-existent item."""
        response = self.client.put(
            reverse("ninja-api:item_update", kwargs={"item_id": 999999}),
            {
                "name": "New Name",
                "price": 9987.00,
                "description": "New Description",
                "store_id": self.store.id,
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_item_update_with_no_token(self) -> None:
        """Test the item update endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.put(
            self.url,
            {
                "name": "New Name",
                "price": 9987.00,
                "description": "New Description",
                "store_id": self.store.id,
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
