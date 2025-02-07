"""Contains the get item API tests."""

import pytest
from requests import Response

from items.tests.api.base_test_case import BaseTestCase

MOCK_ITEM = "Logitech MX Keys Mini"


class ItemGetAPITests(BaseTestCase):
    """Item api tests."""

    def _test_sort(self, response: Response) -> None:
        """Sorting test wrapper."""
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

        self.assertEqual(data.get("total"), 2)

        items = data.get("items")
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].get("name"), "Logitech G Pro X")
        self.assertEqual(items[0].get("price"), "2500.00")
        self.assertEqual(items[1].get("name"), "Very expensive item")
        self.assertEqual(items[1].get("price"), "3000.00")

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    def test_get_items(self) -> None:
        """Test that a user can get items."""
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

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    def test_get_items_with_sort_on_price(self) -> None:
        """Test that a user can get items sorted by price asc."""
        self._login()
        self._create_alt_item()
        url = f"{self.live_server_url}/api/v1/items?sort=price&sort_dir=asc"
        response = self.session.get(url)
        self._test_sort(response)

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    def test_get_items_personal(self) -> None:
        """Test that a user can create an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/me?page=1&per_page=10"
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

    @pytest.mark.skip("Need to fix auth on other tests before this can be fixed")
    def test_get_items_personal_with_sort_on_price(self) -> None:
        """Test that a user can create an item."""
        self._login()
        self._create_alt_item()
        url = f"{self.live_server_url}/api/v1/items/me?sort=price&sort_dir=asc"
        response = self.session.get(url)
        self._test_sort(response)
