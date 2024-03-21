"""Contains the get item API tests."""

from items.tests.api.base_test_case import BaseTestCase

MOCK_ITEM = "Logitech MX Keys Mini"


class ItemGetAPITests(BaseTestCase):
    """Item api tests."""

    def test_get_item(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items?page=1&per_page=10"
        response = self.session.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("items", data)
        self.assertIn("total", data)
        self.assertIn("page_number", data)
        self.assertIn("total_pages", data)
        self.assertIn("has_previous", data)
        self.assertIn("previous_page", data)
        self.assertIn("has_next", data)
        self.assertIn("next_page", data)

        self.assertEqual(data.get("total"), 1)
        self.assertEqual(data.get("page_number"), 1)
        self.assertEqual(data.get("total_pages"), 1)
        self.assertEqual(data.get("has_previous"), False)
        self.assertEqual(data.get("previous_page"), None)
        self.assertEqual(data.get("has_next"), False)
        self.assertEqual(data.get("next_page"), None)

        items = data.get("items")
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].get("name"), "Logitech G Pro X")
        self.assertEqual(items[0].get("description"), "Headphones for gamers.")
        self.assertEqual(items[0].get("price"), "2500.00")
        self.assertEqual(items[0].get("store").get("name"), "Takealot")
        self.assertEqual(items[0].get("user").get("username"), "test")
