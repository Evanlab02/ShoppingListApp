"""Contains the store mapping API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreMappingAPITests(BaseTestCase):
    """Store api tests."""

    def test_store_mapping(self) -> None:
        """Test that a user can get the store type mapping."""
        self._login()
        response = self.session.get(f"{self.live_server_url}/api/v1/stores/types/mapping")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["1"], "Online")
        self.assertEqual(response.json()["2"], "In-Store")
        self.assertEqual(response.json()["3"], "Both")
