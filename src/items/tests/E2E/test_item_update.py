"""Test the item update page."""

import time

from django.contrib.auth.models import User

from items.models import ShoppingItem as Item
from items.tests.E2E.base_test_case import BaseEndToEndTestCase
from stores.models import ShoppingStore as Store


class TestItemUpdateView(BaseEndToEndTestCase):
    """Tests the item update view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        self.item = self._create_test_item(store)
        url = self.live_server_url
        self.url = f"{url}/items/update/{self.item.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_update_page(self) -> None:
        """Test the update page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/update_page.png")

        form_heading = self.driver.find_element(value="form-heading").text
        self.assertEqual(form_heading, "Update Item")

        self.driver.find_element(value="item-input").send_keys("Sony XM4")
        self.driver.find_element(value="price-input").send_keys("600")
        self.driver.get_screenshot_as_file("./screenshots/items/update_page_filled_in.png")

        self.driver.find_element(value="submit-update-item").click()
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/update_page_submitted.png")

        item_name_card = self.driver.find_element(value="item-name-sub-value")
        self.assertEqual(item_name_card.text, "Sony XM4")

        item_price_card = self.driver.find_element(value="item-price-sub-value")
        self.assertEqual(item_price_card.text, "600.00")

        related_lists_card = self.driver.find_element(value="item-related-lists")
        self.assertEqual(related_lists_card.text, "COMING SOON")

        created_by_card = self.driver.find_element(value="user-sub-value")
        self.assertEqual(created_by_card.text, "test")

    def test_update_page_with_error(self) -> None:
        """Test the update page with an error."""
        self.driver.get(f"{self.url}?error=This+is+an+error+message+for+testing+purposes.")
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/items/update_page_with_error.png")

        error_message = self.driver.find_element(value="form-error").text
        self.assertEqual(error_message, "This is an error message for testing purposes.")
