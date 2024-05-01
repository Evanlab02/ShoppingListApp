"""Contains the create item API tests."""

from items.tests.api.base_test_case import BaseTestCase

MOCK_ITEM = "Logitech MX Keys Mini"


class ItemCreateAPITests(BaseTestCase):
    """Item api tests."""

    def test_create_item(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/create"
        payload = {
            "store_id": self.store.id,
            "name": MOCK_ITEM,
            "price": 2500,
            "description": "Minimalist logitech keyboard.",
        }
        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        user = response_json.get("user")
        username = user.get("username")
        self.assertEqual(username, self.user.username)

        store = response_json.get("store")
        store_name = store.get("name")
        self.assertEqual(store_name, "Takealot")

        name = response_json.get("name")
        description = response_json.get("description")
        price = response_json.get("price")

        self.assertEqual(name, MOCK_ITEM)
        self.assertEqual(description, "Minimalist logitech keyboard.")
        self.assertEqual(price, "2500.0")

    def test_create_item_no_description(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/create"
        payload = {
            "store_id": self.store.id,
            "name": MOCK_ITEM,
            "price": 2500,
        }
        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        description = response_json.get("description")

        self.assertEqual(description, "")

    def test_create_item_duplicate(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/create"
        payload = {
            "store_id": self.store.id,
            "name": "Logitech G Pro X",
            "price": 2500,
        }
        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 400)

    def test_create_item_store_does_not_exist(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/create"
        payload = {
            "store_id": 99999,
            "name": MOCK_ITEM,
            "price": 2500,
        }
        response = self.session.post(url, json=payload)
        self.assertEqual(response.status_code, 404)
