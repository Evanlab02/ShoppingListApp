"""Test the item create page."""

import time

from selenium.webdriver.support.select import Select

from items.models import ShoppingItem as Item
from items.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestItemCreateView(BaseEndToEndTestCase):
    """Tests the item create view with E2E tests."""

    def test_get_create_item(self) -> None:
        """Test the create item page."""
        url = self.live_server_url

        self._login_self()
        self.driver.get(f"{url}/items/create")
        time.sleep(1)

        self.driver.get_screenshot_as_file("./screenshots/items/create_page.png")
        heading = self.driver.find_element(value="form-heading").text
        self.assertEqual(heading, "Create Item")

        tag_name = self.driver.find_element(value="store-input").tag_name
        self.assertEqual(tag_name, "select")

        tag_name = self.driver.find_element(value="item-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="description-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="price-input").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="submit-create-item").tag_name
        self.assertEqual(tag_name, "input")

        tag_name = self.driver.find_element(value="cancel-create-item").tag_name
        self.assertEqual(tag_name, "input")

    def test_create_item(self) -> None:
        """Test creating an item."""
        url = self.live_server_url
        self._login_self()
        self.driver.get(f"{url}/items/create")

        self.driver.find_element(value="item-input").send_keys("Sony XM4")
        self.driver.find_element(value="price-input").send_keys("600")
        select = Select(self.driver.find_element(value="store-input"))
        select.select_by_index(0)

        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/create_page_filled_in.png")

        self.driver.find_element(value="submit-create-item").click()
        items = Item.objects.all()
        self.assertEqual(1, len(items))

    def test_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create item page without being logged in."""
        url = self.live_server_url
        self.driver.get(f"{url}/items/create")
        self.driver.get_screenshot_as_file("./screenshots/items/create_page_no_login.png")
        self.assertEqual(
            self.driver.current_url,
            f"{url}/?error=You%20must%20be%20logged%20in%20to%20access%20that%20page.",
        )

    def test_get_create_page_with_error(self) -> None:
        """Test that a user can access the create item page with an error."""
        self._login_self()
        url = self.live_server_url
        self.driver.get(f"{url}/items/create?error=This+is+an+error")
        self.assertEqual(self.driver.current_url, f"{url}/items/create?error=This+is+an+error")

        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/create_page_with_error.png")
        error_text = self.driver.find_element(value="form-error").text
        self.assertEqual(error_text, "This is an error")
