"""Test the store update page."""

import time

from stores.models import ShoppingStore as Store
from stores.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestStoreUpdateView(BaseEndToEndTestCase):
    """Tests the store update view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        url = self.live_server_url
        self.url = f"{url}/stores/update/{store.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Store.objects.all().delete()
        return super().tearDown()

    def test_update_page(self) -> None:
        """Test the update page."""
        self.driver.get(self.url)
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/stores/update_page.png")
        self.driver.find_element(value="store-input").send_keys("Store Has Been Updated")
        self.driver.find_element(value="store-type-input").send_keys("Online")
        self.driver.find_element(value="description-input").send_keys("Test Description Updated")
        self.driver.find_element(value="submit-update-store").click()

        self.assertEqual(
            self.driver.find_element(value="store-name-sub-value").text, "Store Has Been Updated"
        )
        self.driver.get_screenshot_as_file("./screenshots/stores/post_update_page.png")
