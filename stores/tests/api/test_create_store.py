"""Contains the create store API tests."""

from stores.tests.api.base_test_case import BaseTestCase


class StoreCreateAPITests(BaseTestCase):
    """Store api tests."""

    def test_create_store(self) -> None:
        """Test that a user can create a store."""
        self._login()
        url = f"{self.live_server_url}/api/v1/stores/create"
        payload = {
            "name": "StoreTester1",
            "description": "StoreTester1",
            "store_type": 3,
        }
        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "StoreTester1")
        self.assertEqual(response.json()["description"], "StoreTester1")
        self.assertEqual(response.json()["store_type"], 3)
        self.assertIsInstance(response.json()["id"], int)
        self.assertIsInstance(response.json()["created_at"], str)
        self.assertIsInstance(response.json()["updated_at"], str)
