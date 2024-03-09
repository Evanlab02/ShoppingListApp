"""Contains the store delete API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreDeleteAPITests(BaseTestCase):
    """Store api tests."""

    def test_delete_store(self) -> None:
        """Test that a use can delete the store."""
        self._login()
        store_delete_response = self.session.delete(
            f"{self.live_server_url}/api/v1/stores/delete/{self.store.id}"
        )
        self.assertEqual(store_delete_response.status_code, 200)

        response_json = store_delete_response.json()
        self.assertEqual(response_json.get("message"), "Deleted Store.")
        self.assertEqual(
            response_json.get("detail"), f"Store with ID #{self.store.id} was deleted."
        )
