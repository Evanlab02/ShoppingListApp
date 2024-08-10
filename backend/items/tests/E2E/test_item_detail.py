"""Test the item detail page."""

import time

from django.contrib.auth.models import User

from items.models import ShoppingItem as Item
from items.tests.E2E.base_test_case import BaseEndToEndTestCase
from stores.models import ShoppingStore as Store


class TestItemOverviewView(BaseEndToEndTestCase):
    """Tests the item overview view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        self.item = self._create_test_item(store)
        url = self.live_server_url
        self.url = f"{url}/items/detail/{self.item.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_detail_page(self) -> None:
        """Test the detail page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/detail_page.png")

        item_name = self.driver.find_element(value="item-name-sub-value").text
        self.assertEqual(item_name, "Test Item")

        item_store_name = self.driver.find_element(value="item-store-sub-value").text
        self.assertEqual(item_store_name, "Test Store")

        item_price = self.driver.find_element(value="item-price-sub-value").text
        self.assertEqual(item_price, "100.00")

        related_lists_number = self.driver.find_element(value="item-related-lists").text
        self.assertEqual(related_lists_number, "COMING SOON")

        item_user = self.driver.find_element(value="user-sub-value").text
        self.assertEqual(item_user, "test")
