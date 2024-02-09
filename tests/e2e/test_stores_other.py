"""
Contains end-to-end tests for the store pages.
"""

from selenium.webdriver.common.by import By

from tests.e2e.other_base_test_case import AlternativeBaseTestCase

# Urls
STORE_OVERVIEW_URL = "http://localhost:7001/stores/me"


class TestStorePages(AlternativeBaseTestCase):
    """Contains end-to-end tests for the store app pages for the alternative user."""

    def test_01_personal_store_overview_page(self) -> None:
        """Test the store overview page."""
        self._login()
        self.driver.get(STORE_OVERVIEW_URL)

        self.driver.get_screenshot_as_file("./screenshots/stores/empty_overview.png")
        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "0")

        total_in_store_stores = self.driver.find_element(value="total-in-stores-sub-value").text
        self.assertEqual(total_in_store_stores, "0 (0)")

        total_online_stores = self.driver.find_element(value="total-online-stores-sub-value").text
        self.assertEqual(total_online_stores, "0 (0)")

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="store-table-row")
        self.assertEqual(len(rows), 0)
