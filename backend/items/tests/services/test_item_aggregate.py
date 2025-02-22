"""Contains tests for the item aggregate service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemAggregateServiceTestCase(TestCase):
    """Tests for the item aggregate service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.items = ItemFactory.create_batch(size=10, store=self.store, user=self.user)

    async def test_aggregate_items(self) -> None:
        """Test the aggregate items method."""
        aggregation = await self.item_service.aggregate(user=self.user)
        self.assertEqual(aggregation.total_items, 10)
        self.assertEqual(aggregation.total_price, sum([item.price for item in self.items]))
        self.assertEqual(aggregation.average_price, sum([item.price for item in self.items]) / 10)
        self.assertEqual(aggregation.max_price, max([item.price for item in self.items]))
        self.assertEqual(aggregation.min_price, min([item.price for item in self.items]))
