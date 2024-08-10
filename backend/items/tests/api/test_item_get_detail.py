"""Contains the detail item API tests."""

from items.tests.api.base_test_case import BaseTestCase


class ItemDetailAPITests(BaseTestCase):
    """Item api tests."""

    def test_get_item_detail(self) -> None:
        """Test getting an item detail."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/detail/{self.item.id}"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)

        item = response.json()
        self.assertEqual(item["name"], self.item.name)
        self.assertEqual(item["price"], "2500.00")
        self.assertEqual(item["description"], self.item.description)

        self.assertEqual(item["store"]["name"], self.store.name)
        self.assertEqual(item["user"]["username"], self.user.username)

    def test_get_item_detail_not_found(self) -> None:
        """Test getting an item detail that does not exist."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/detail/100"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Item with id '100' does not exist."})
