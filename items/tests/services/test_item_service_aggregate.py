"""Contains tests for the item service aggregate function."""

from items.services import item_service
from items.tests.base.base_test_case import BaseTestCase


class TestAggregationService(BaseTestCase):
    """Test the item service aggregation functions."""

    async def test_aggregate_items(self) -> None:
        """Test that the items are aggregated."""
        aggregation = await item_service.aggregate()
        self.assertEqual(aggregation.total_items, 2)
        self.assertEqual(aggregation.total_price, 300)
        self.assertEqual(aggregation.average_price, 150)
        self.assertEqual(aggregation.max_price, 200)
        self.assertEqual(aggregation.min_price, 100)
