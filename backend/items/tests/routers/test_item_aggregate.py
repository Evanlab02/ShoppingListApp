"""Tests for the item aggregate router."""

from django.urls import reverse

from items.tests.factory import ItemFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class ItemAggregateRouterTestCase(BaseRouterTestCase):
    """Tests for the item aggregate router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()

        self.store = StoreFactory.create(user=self.user)
        self.items = ItemFactory.create_batch(10, store=self.store)
        self.items_me = ItemFactory.create_batch(10, user=self.user)

        self.prices = [item.price for item in self.items]
        self.prices_me = [item.price for item in self.items_me]
        self.prices_all = self.prices + self.prices_me

        self.total_price = sum(self.prices)
        self.total_price_me = sum(self.prices_me)
        self.total_price_all = self.total_price + self.total_price_me

        self.average_price_all = self.total_price_all / (len(self.items) + len(self.items_me))
        self.max_price_all = max(self.prices_all)
        self.min_price_all = min(self.prices_all)

        self.average_price_me = self.total_price_me / len(self.items_me)
        self.max_price_me = max(self.prices_me)
        self.min_price_me = min(self.prices_me)

        self.url = reverse("ninja-api:item_aggregate")
        self.url_me = reverse("ninja-api:item_aggregate_me")

    def test_aggregate(self) -> None:
        """Test the aggregate endpoint."""
        response = self.client.get(
            self.url, content_type=self.content_type, headers=self.base_headers
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["total_items"], 20)
        self.assertEqual(response_json["total_price"], self.total_price_all)
        self.assertEqual(response_json["average_price"], self.average_price_all)
        self.assertEqual(response_json["max_price"], self.max_price_all)
        self.assertEqual(response_json["min_price"], self.min_price_all)

    def test_aggregate_me(self) -> None:
        """Test the aggregate endpoint for the current user."""
        response = self.client.get(
            self.url_me, content_type=self.content_type, headers=self.base_headers
        )
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["total_items"], 10)
        self.assertEqual(response_json["total_price"], self.total_price_me)
        self.assertEqual(response_json["average_price"], self.average_price_me)
        self.assertEqual(response_json["max_price"], self.max_price_me)
        self.assertEqual(response_json["min_price"], self.min_price_me)
