"""Test the item overview page."""

import time

from django.contrib.auth.models import User
from selenium.webdriver.common.by import By

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
        self._create_test_item(store)
        url = self.live_server_url
        self.url = f"{url}/items/"

    def tearDown(self) -> None:
        """Tear down the test."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_overview_page(self) -> None:
        """Test the overview page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/overview_page.png")

        total_items = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_items, "1")

        total_in_store_stores = self.driver.find_element(value="total-price-sub-value").text
        self.assertEqual(total_in_store_stores, "100.0")

        total_online_stores = self.driver.find_element(value="average-price-sub-value").text
        self.assertEqual(total_online_stores, "100.0")

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="item-table-row")
        self.assertEqual(len(rows), 1)

    def test_personal_overview_page(self) -> None:
        """Test the personal overview page."""
        self.driver.get(f"{self.url}me")
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/personal_overview_page.png")

        total_items = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_items, "1")

        total_in_store_stores = self.driver.find_element(value="total-price-sub-value").text
        self.assertEqual(total_in_store_stores, "100.0")

        total_online_stores = self.driver.find_element(value="average-price-sub-value").text
        self.assertEqual(total_online_stores, "100.0")

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="item-table-row")
        self.assertEqual(len(rows), 1)
