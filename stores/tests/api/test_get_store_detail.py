"""Contains the store detail API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreDetailAPITests(BaseTestCase):
    """Store api tests."""

    def test_get_store_detail(self) -> None:
        """Test that a user can get the store detail."""
        response = self.session.get(f"{self.live_server_url}/api/v1/stores/detail/{self.store.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Store")
        self.assertEqual(response.json()["description"], "")
        self.assertEqual(response.json()["store_type"], 1)
        self.assertIsInstance(response.json()["id"], int)
        self.assertIsInstance(response.json()["created_at"], str)
        self.assertIsInstance(response.json()["updated_at"], str)
        self.assertEqual(response.json()["user"]["username"], "test")

    def test_get_store_detail_invalid_id(self) -> None:
        """Test that a user can get the store detail."""
        response = self.session.get(f"{self.live_server_url}/api/v1/stores/detail/99999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Store with id '99999' does not exist.")
