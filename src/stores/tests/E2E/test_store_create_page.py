"""Test the store create page."""

from selenium.webdriver.support.select import Select

from stores.models import ShoppingStore as Store
from stores.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestStoreCreateView(BaseEndToEndTestCase):
    """Tests the store create view with E2E tests."""

    def test_get_create_store(self) -> None:
        """Test the create store page."""
        url = self.live_server_url

        self._login_self()
        self.driver.get(f"{url}/stores/create")

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

    def test_create_store(self) -> None:
        """Test creating a store."""
        url = self.live_server_url
        self._login_self()
        self.driver.get(f"{url}/stores/create")

        self.driver.find_element(value="store-input").send_keys("Takealot")
        select = Select(self.driver.find_element(value="store-type-input"))
        select.select_by_index(0)
        self.driver.find_element(value="submit-create-store").click()

        stores = Store.objects.all()
        self.assertEqual(1, len(stores))

    def test_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create store page without being logged in."""
        url = self.live_server_url
        self.driver.get(f"{url}/stores/create")
        self.driver.get_screenshot_as_file("./screenshots/stores/create_page_no_login.png")
        self.assertEqual(
            self.driver.current_url,
            f"{url}/?error=You%20must%20be%20logged%20in%20to%20access%20that%20page.",
        )

    def test_get_create_page_with_error(self) -> None:
        """Test that a user can access the create store page with an error."""
        self._login_self()
        url = self.live_server_url
        self.driver.get(f"{url}/stores/create?error=This+is+an+error")
        self.assertEqual(self.driver.current_url, f"{url}/stores/create?error=This+is+an+error")

        self.driver.get_screenshot_as_file("./screenshots/stores/create_page_with_error.png")
        error_text = self.driver.find_element(value="form-error").text
        self.assertEqual(error_text, "This is an error")
