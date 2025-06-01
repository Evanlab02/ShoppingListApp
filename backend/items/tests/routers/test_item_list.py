"""Test the item list endpoints."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class ItemListRouterTestCase(BaseRouterTestCase):
    """Test the item list endpoints."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.list_url = reverse("ninja-api:item_list")
        self.list_me_url = reverse("ninja-api:item_list_me")
        self.search_url = reverse("ninja-api:item_search")

        self.store = StoreFactory.create(user=self.user)

        self.items = ItemFactory.create_batch(10)
        self.items_me = ItemFactory.create_batch(10, user=self.user)
        self.items_store = ItemFactory.create_batch(10, store=self.store)

    def test_list_items(self) -> None:
        """Test the list items endpoint."""
        response = self.client.get(
            self.list_url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 10)

        for item in response.json()["items"]:
            self.assertIn(
                item["id"],
                [item.id for item in self.items]
                + [item.id for item in self.items_me]
                + [item.id for item in self.items_store],
            )

    def test_list_items_me(self) -> None:
        """Test the list items endpoint for the current user."""
        response = self.client.get(
            self.list_me_url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 10)

        for item in response.json()["items"]:
            self.assertIn(item["id"], [item.id for item in self.items_me])

    def test_search_items(self) -> None:
        """Test the search endpoint for a specific store."""
        response = self.client.post(
            self.search_url,
            {"store": self.store.id},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 10)

        for item in response.json()["items"]:
            self.assertIn(item["id"], [item.id for item in self.items_store])

    def test_search_items_me(self) -> None:
        """Test the search endpoint for the current user."""
        response = self.client.post(
            f"{self.search_url}?own=true",
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 10)

        for item in response.json()["items"]:
            self.assertIn(item["id"], [item.id for item in self.items_me])

    def test_list_items_with_no_token(self) -> None:
        """Test the list items endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.list_url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_list_my_items_with_no_token(self) -> None:
        """Test the list my items endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.list_me_url,
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_search_items_with_no_token(self) -> None:
        """Test the search endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.post(
            self.search_url,
            {"store": self.store.id},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
