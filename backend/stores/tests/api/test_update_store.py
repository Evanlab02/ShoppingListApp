"""Contains the store update API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreUpdateAPITests(BaseTestCase):
    """Store api tests."""

    def test_update_store(self) -> None:
        """Test that a user can update the store."""
        self._login()
        store_update_response = self.session.patch(
            f"{self.live_server_url}/api/v1/stores/update/{self.store.id}?store_type=3"
        )
        self.assertEqual(store_update_response.status_code, 200)

        response_json = store_update_response.json()
        self.assertEqual(response_json.get("id"), self.store.id)
        self.assertEqual(response_json.get("name"), self.store.name)
        self.assertEqual(response_json.get("store_type"), 3)
        self.assertEqual(response_json.get("description"), self.store.description)
