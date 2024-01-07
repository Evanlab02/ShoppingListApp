"""Contains tests for the aggregation endpoint of the stores app."""

from django.test import Client, TestCase


class TestAggregation(TestCase):
    """Contains tests for the aggregation endpoint."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = Client()

    def test_aggregation(self) -> None:
        """Test the aggregation endpoint."""
        result = self.client.get("/api/v1/stores/aggregate")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total_stores"], 0)
        self.assertEqual(result_json["online_stores"], 0)
        self.assertEqual(result_json["in_store_stores"], 0)
        self.assertEqual(result_json["combined_stores"], 0)
        self.assertEqual(result_json["combined_online_stores"], 0)
        self.assertEqual(result_json["combined_in_store_stores"], 0)
