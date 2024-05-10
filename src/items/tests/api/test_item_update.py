"""Contains the update item api tests."""

from items.tests.api.base_test_case import BaseTestCase


class ItemUpdateAPITests(BaseTestCase):
    """Item api tests."""

    def test_update_item(self) -> None:
        """Test that the item is updated."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/update/{self.item.id}"
        data = {
            "name": "Updated Item",
            "price": 2000,
            "description": "Updated Description",
            "store_id": self.store.id,
        }
        response = self.session.patch(url, json=data)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], "Updated Item")
        self.assertEqual(response_json["price"], "2000.0")
        self.assertEqual(response_json["description"], "Updated Description")
        self.assertEqual(response_json["store"]["id"], self.store.id)
