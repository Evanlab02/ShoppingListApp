"""Test the store detail page."""

import time

from selenium.webdriver.common.by import By

from stores.models import ShoppingStore as Store
from stores.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestStoreDetailView(BaseEndToEndTestCase):
    """Tests the store detail view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        self._create_test_item(store)
        url = self.live_server_url
        self.url = f"{url}/stores/detail/{store.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Store.objects.all().delete()
        return super().tearDown()

    def test_detail_page(self) -> None:
        """Test the detail page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/stores/detail_page.png")
        self.assertEqual(self.driver.find_element(value="store-name-sub-value").text, "Test Store")
        self.assertEqual(self.driver.find_element(value="store-type-sub-value").text, "Online")
        self.assertEqual(
            self.driver.find_element(value="number-of-items-sub-value").text,
            "1",
        )
        self.assertEqual(self.driver.find_element(value="user-sub-value").text, "test")

        row_elements = self.driver.find_elements(by=By.CLASS_NAME, value="store-item-row")
        self.assertEqual(len(row_elements), 1)
