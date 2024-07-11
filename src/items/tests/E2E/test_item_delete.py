"""Test the item delete page."""

import time

from django.contrib.auth.models import User

from items.models import ShoppingItem as Item
from items.tests.E2E.base_test_case import BaseEndToEndTestCase
from stores.models import ShoppingStore as Store


class TestItemDeleteView(BaseEndToEndTestCase):
    """Tests the item delete view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        self.item = self._create_test_item(store)
        url = self.live_server_url
        self.url = f"{url}/items/delete/{self.item.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_delete_page(self) -> None:
        """Test the delete page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/delete_page.png")

        form_heading = self.driver.find_element(value="form-heading").text
        self.assertEqual(form_heading, "Delete Item")

        self.driver.find_element(value="submit-delete-item").click()
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/delete_page_submit.png")

    def test_delete_page_with_error(self) -> None:
        """Test the update page with an error."""
        self.driver.get(f"{self.url}?error=This+is+an+error+message+for+testing+purposes.")
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/delete_page_with_error.png")

        error_message = self.driver.find_element(value="form-error").text
        self.assertEqual(error_message, "This is an error message for testing purposes.")
