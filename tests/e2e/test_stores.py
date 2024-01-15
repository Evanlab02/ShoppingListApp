"""
Contains end-to-end tests for the store pages.
"""

from selenium.webdriver.common.by import By

from tests.e2e.base_test_case import BaseTestCase

# Urls
STORE_CREATE_URL = "http://localhost:7001/stores/create"
STORE_OVERVIEW_URL = "http://localhost:7001/stores/"
LOGIN_URL = "http://localhost:7001/"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
ERROR_TEXT = "error-text"


class TestStorePages(BaseTestCase):
    """Contains end-to-end tests for the store create page."""

    def test_01_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create store page without being logged in."""
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(
            self.driver.current_url,
            f"{LOGIN_URL}?error=You%20must%20be%20logged%20in%20to%20access%20that%20page.",
        )

    def test_02_get_create_page(self) -> None:
        """Test that a user can access the create store page."""
        self._login()
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(self.driver.current_url, STORE_CREATE_URL)

        heading = self.driver.find_element(value="form-heading").text
        self.assertEqual(heading, "Create Store")

        tag_name = self.driver.find_element(value="store-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="store-type-input").tag_name
        self.assertEqual(tag_name, "select")

        tag_name = self.driver.find_element(value="description-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="submit-create-store").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="cancel-create-store").tag_name
        self.assertEqual(tag_name, "input")

    def test_03_get_create_page_with_error(self) -> None:
        """Test that a user can access the create store page with an error."""
        self.driver.get(f"{STORE_CREATE_URL}?error=This+is+an+error")
        self.assertEqual(self.driver.current_url, f"{STORE_CREATE_URL}?error=This+is+an+error")

        error_text = self.driver.find_element(value="form-error").text
        self.assertEqual(error_text, "This is an error")

    def test_04_create_store(self) -> None:
        """Test that a user can create a store."""
        self.driver.get(STORE_CREATE_URL)

        self.driver.find_element(value="store-input").send_keys("Test Store")
        self.driver.find_element(value="store-type-input").send_keys("Both")
        self.driver.find_element(value="description-input").send_keys("Test Description")
        self.driver.find_element(value="submit-create-store").click()

        current_url = self.driver.current_url
        self.assertTrue(current_url.startswith("http://localhost:7001/stores/detail/"))

    def test_05_store_detail_page(self) -> None:
        """Test the store detail page."""
        self.assertEqual(self.driver.find_element(value="store-name-sub-value").text, "Test Store")
        self.assertEqual(
            self.driver.find_element(value="store-type-sub-value").text, "Online & In-Store"
        )
        self.assertEqual(
            self.driver.find_element(value="number-of-items-sub-value").text, "COMING SOON"
        )
        self.assertEqual(self.driver.find_element(value="user-sub-value").text, "basetestuser1")

        row_elements = self.driver.find_elements(by=By.CLASS_NAME, value="store-item-row")
        self.assertEqual(len(row_elements), 0)

    def test_06_store_overview_page(self) -> None:
        """Test the store overview page."""
        self.driver.get(STORE_OVERVIEW_URL)

        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "3")
