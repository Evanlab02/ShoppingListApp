"""Test the store overview page."""

import time

from selenium.webdriver.common.by import By

from stores.models import ShoppingStore as Store
from stores.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestStoreOverviewView(BaseEndToEndTestCase):
    """Tests the store overview view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        self._create_test_store()
        url = self.live_server_url
        self.url = f"{url}/stores/"

    def tearDown(self) -> None:
        """Tear down the test."""
        Store.objects.all().delete()
        return super().tearDown()

    def test_overview_page(self) -> None:
        """Test the overview page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/stores/overview_page.png")

        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "1")

        total_in_store_stores = self.driver.find_element(value="total-in-stores-sub-value").text
        self.assertEqual(total_in_store_stores, "0 (0)")

        total_online_stores = self.driver.find_element(value="total-online-stores-sub-value").text
        self.assertEqual(total_online_stores, "1 (1)")

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="store-table-row")
        self.assertEqual(len(rows), 1)

    def test_overview_page_personal(self) -> None:
        """Test the personal overview page."""
        self.driver.get(f"{self.url}me")
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/stores/personal_overview_page.png")

        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "1")

        total_in_store_stores = self.driver.find_element(value="total-in-stores-sub-value").text
        self.assertEqual(total_in_store_stores, "0 (0)")

        total_online_stores = self.driver.find_element(value="total-online-stores-sub-value").text
        self.assertEqual(total_online_stores, "1 (1)")

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="store-table-row")
        self.assertEqual(len(rows), 1)
