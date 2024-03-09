"""Contains the store aggregation API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreAggregationAPITests(BaseTestCase):
    """Store api tests."""

    def test_get_store_aggregation(self) -> None:
        """Test that a user can get the store aggregation."""
        response = self.session.get(f"{self.live_server_url}/api/v1/stores/aggregate")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["total_stores"], int)
        self.assertIsInstance(response.json()["online_stores"], int)
        self.assertIsInstance(response.json()["in_store_stores"], int)
        self.assertIsInstance(response.json()["combined_stores"], int)
        self.assertIsInstance(response.json()["combined_online_stores"], int)
        self.assertIsInstance(response.json()["combined_in_store_stores"], int)

    def test_get_store_aggregation_personal(self) -> None:
        """Test that a user can get the store aggregation."""
        self._login()
        response = self.session.get(f"{self.live_server_url}/api/v1/stores/aggregate/me")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json()["total_stores"], int)
        self.assertIsInstance(response.json()["online_stores"], int)
        self.assertIsInstance(response.json()["in_store_stores"], int)
        self.assertIsInstance(response.json()["combined_stores"], int)
        self.assertIsInstance(response.json()["combined_online_stores"], int)
        self.assertIsInstance(response.json()["combined_in_store_stores"], int)
