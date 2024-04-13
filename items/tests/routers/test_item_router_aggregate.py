"""Contains tests for the item router aggregate function."""

from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestAggregationRouter(BaseTestCase):
    """Test the item router aggregation functions."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        return super().setUp()

    def test_aggregate_items(self) -> None:
        """Test that the items are aggregated."""
        response = self.client.get("/api/v1/items/aggregate")
        aggregation = response.json()
        self.assertEqual(aggregation["total_items"], 2)
        self.assertEqual(aggregation["total_price"], 300)
        self.assertEqual(aggregation["average_price"], 150)
        self.assertEqual(aggregation["max_price"], 200)
        self.assertEqual(aggregation["min_price"], 100)
