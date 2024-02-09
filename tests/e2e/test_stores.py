"""
Contains end-to-end tests for the store pages.
"""

from selenium.webdriver.common.by import By

from tests.e2e.base_test_case import BaseTestCase

# Urls
STORE_CREATE_URL = "http://localhost:7001/stores/create"
STORE_OVERVIEW_URL = "http://localhost:7001/stores/"
PERSONAL_STORE_OVERVIEW_URL = "http://localhost:7001/stores/me"
LOGIN_URL = "http://localhost:7001/"
DETAIL_URL = "http://localhost:7001/stores/detail/"

IN_STORE_INFO_CARD_TEXT = "0 (2)"
ONLINE_INFO_CARD_TEXT = "0 (2)"

COMING_SOON_PLACEHOLDER = "COMING SOON"


class TestStorePages(BaseTestCase):
    """Contains end-to-end tests for the store create page."""

    def test_01_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create store page without being logged in."""
        self.driver.get(STORE_CREATE_URL)
        self.driver.get_screenshot_as_file("./screenshots/stores/create_page_no_login.png")
        self.assertEqual(
            self.driver.current_url,
            f"{LOGIN_URL}?error=You%20must%20be%20logged%20in%20to%20access%20that%20page.",
        )

    def test_02_get_create_page(self) -> None:
        """Test that a user can access the create store page."""
        self._login()
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(self.driver.current_url, STORE_CREATE_URL)

        self.driver.get_screenshot_as_file("./screenshots/stores/create_page.png")
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

        self.driver.get_screenshot_as_file("./screenshots/stores/create_page_with_error.png")
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
        self.assertTrue(current_url.startswith(DETAIL_URL))

    def test_05_store_detail_page(self) -> None:
        """Test the store detail page."""
        self.driver.get_screenshot_as_file("./screenshots/stores/detail_page.png")
        self.assertEqual(self.driver.find_element(value="store-name-sub-value").text, "Test Store")
        self.assertEqual(
            self.driver.find_element(value="store-type-sub-value").text, "Online & In-Store"
        )
        self.assertEqual(
            self.driver.find_element(value="number-of-items-sub-value").text,
            COMING_SOON_PLACEHOLDER,
        )
        self.assertEqual(self.driver.find_element(value="user-sub-value").text, "basetestuser1")

        row_elements = self.driver.find_elements(by=By.CLASS_NAME, value="store-item-row")
        self.assertEqual(len(row_elements), 0)

    def test_06_store_overview_page(self) -> None:
        """Test the store overview page."""
        self.driver.get(STORE_OVERVIEW_URL)
        self.driver.get_screenshot_as_file("./screenshots/stores/overview_page.png")

        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "2")

        total_in_store_stores = self.driver.find_element(value="total-in-stores-sub-value").text
        self.assertEqual(total_in_store_stores, IN_STORE_INFO_CARD_TEXT)

        total_online_stores = self.driver.find_element(value="total-online-stores-sub-value").text
        self.assertEqual(total_online_stores, ONLINE_INFO_CARD_TEXT)

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="store-table-row")
        self.assertEqual(len(rows), 2)

    def test_07_personal_store_overview_page(self) -> None:
        """Test the store overview page."""
        self.driver.get(PERSONAL_STORE_OVERVIEW_URL)
        self.driver.get_screenshot_as_file("./screenshots/stores/personaL_overview_page.png")

        total_stores = self.driver.find_element(value="total-items-sub-value").text
        self.assertEqual(total_stores, "2")

        total_in_store_stores = self.driver.find_element(value="total-in-stores-sub-value").text
        self.assertEqual(total_in_store_stores, IN_STORE_INFO_CARD_TEXT)

        total_online_stores = self.driver.find_element(value="total-online-stores-sub-value").text
        self.assertEqual(total_online_stores, ONLINE_INFO_CARD_TEXT)

        rows = self.driver.find_elements(by=By.CLASS_NAME, value="store-table-row")
        self.assertEqual(len(rows), 2)

    def test_08_update_store(self) -> None:
        self.driver.get(STORE_CREATE_URL)

        self.driver.find_element(value="store-input").send_keys("Store For Update")
        self.driver.find_element(value="store-type-input").send_keys("Both")
        self.driver.find_element(value="description-input").send_keys("Test Description")
        self.driver.find_element(value="submit-create-store").click()

        current_url = self.driver.current_url
        self.assertTrue(current_url.startswith(DETAIL_URL))

        store_id = current_url.replace(DETAIL_URL, "")

        self.assertEqual(
            self.driver.find_element(value="store-name-sub-value").text, "Store For Update"
        )
        self.assertEqual(
            self.driver.find_element(value="store-type-sub-value").text, "Online & In-Store"
        )
        self.assertEqual(
            self.driver.find_element(value="number-of-items-sub-value").text,
            COMING_SOON_PLACEHOLDER,
        )
        self.assertEqual(self.driver.find_element(value="user-sub-value").text, "basetestuser1")

        row_elements = self.driver.find_elements(by=By.CLASS_NAME, value="store-item-row")
        self.assertEqual(len(row_elements), 0)

        self.driver.get(f"http://localhost:7001/stores/update/{store_id}")

        self.driver.get_screenshot_as_file("./screenshots/stores/update_page.png")
        self.driver.find_element(value="store-input").send_keys("Store Has Been Updated")
        self.driver.find_element(value="store-type-input").send_keys("Online")
        self.driver.find_element(value="description-input").send_keys("Test Description Updated")
        self.driver.find_element(value="submit-update-store").click()

        self.assertEqual(
            self.driver.find_element(value="store-name-sub-value").text, "Store Has Been Updated"
        )
        self.assertEqual(self.driver.find_element(value="store-type-sub-value").text, "Online")
        self.assertEqual(
            self.driver.find_element(value="number-of-items-sub-value").text,
            COMING_SOON_PLACEHOLDER,
        )
        self.assertEqual(self.driver.find_element(value="user-sub-value").text, "basetestuser1")

        row_elements = self.driver.find_elements(by=By.CLASS_NAME, value="store-item-row")
        self.assertEqual(len(row_elements), 0)
