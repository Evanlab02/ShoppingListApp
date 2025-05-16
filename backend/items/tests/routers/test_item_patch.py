"""Test the item patch endpoint."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


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

    def test_item_patch_store_id(self) -> None:
        """Test patching an item's store_id."""
        new_store = StoreFactory.create(user=self.user)
        response = self.client.patch(
            self.url,
            {"store_id": new_store.id},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["store"]["id"], new_store.id)

    def test_item_patch_price(self) -> None:
        """Test patching an item's price."""
        new_price = 99.99
        response = self.client.patch(
            self.url,
            {"price": new_price},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["price"], str(new_price))

    def test_item_patch_description(self) -> None:
        """Test patching an item's description."""
        new_description = "Updated description"
        response = self.client.patch(
            self.url,
            {"description": new_description},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], new_description)

    def test_item_patch_all_fields(self) -> None:
        """Test patching all fields of an item at once."""
        new_store = StoreFactory.create(user=self.user)
        patch_data = {
            "store_id": new_store.id,
            "name": "Updated Name",
            "price": 149.99,
            "description": "Updated description for all fields",
        }
        response = self.client.patch(
            self.url,
            patch_data,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["store"]["id"], new_store.id)
        self.assertEqual(response_data["name"], "Updated Name")
        self.assertEqual(response_data["price"], "149.99")
        self.assertEqual(response_data["description"], "Updated description for all fields")
