"""Contains tests for the item create router."""

from django.urls import reverse

from items.models import ShoppingItem as Item
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class ItemCreateRouterTestCase(BaseRouterTestCase):
    """Contains tests for the item create router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.url = reverse("ninja-api:item_create")

    def test_create_item(self) -> None:
        """Test the create item endpoint."""
        response = self.client.post(
            self.url,
            {"name": "Test Item", "price": 100, "store_id": self.store.id},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        # Test status code
        self.assertEqual(response.status_code, 201)

        # Test response data
        response_json = response.json()
        actual_name = response_json["name"]
        actual_price = response_json["price"]
        actual_store_id = response_json["store"]["id"]

        self.assertEqual(actual_name, "Test Item")
        self.assertEqual(actual_price, "100.0")
        self.assertEqual(actual_store_id, self.store.id)

        # Test DB content
        item = Item.objects.get(id=response_json["id"])
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 100)
        self.assertEqual(item.store.id, self.store.id)

    def test_create_item_with_no_token(self) -> None:
        """Test the create item endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.post(
            self.url,
            {"name": "Test Item", "price": 100, "store_id": self.store.id},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        # Test status code
        self.assertEqual(response.status_code, 401)
