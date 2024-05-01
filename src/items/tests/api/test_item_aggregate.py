"""Contains the aggregate item API tests."""

from items.tests.api.base_test_case import BaseTestCase


class ItemAggregateAPITests(BaseTestCase):
    """Item api tests."""

    def test_aggregate_items(self) -> None:
        """Test that the items are aggregated."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/aggregate"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["total_items"], 1)
        self.assertEqual(response_json["total_price"], 2500)
        self.assertEqual(response_json["average_price"], 2500)
        self.assertEqual(response_json["max_price"], 2500)
        self.assertEqual(response_json["min_price"], 2500)

    def test_aggregate_personal_items(self) -> None:
        """Test that the personal items are aggregated."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/aggregate/me"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["total_items"], 1)
        self.assertEqual(response_json["total_price"], 2500)
        self.assertEqual(response_json["average_price"], 2500)
        self.assertEqual(response_json["max_price"], 2500)
        self.assertEqual(response_json["min_price"], 2500)
