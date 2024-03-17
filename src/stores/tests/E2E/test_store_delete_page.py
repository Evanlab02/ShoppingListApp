"""Test the store delete page."""

import time

from stores.models import ShoppingStore as Store
from stores.tests.E2E.base_test_case import BaseEndToEndTestCase


class TestStoreDeleteView(BaseEndToEndTestCase):
    """Tests the store delete view with E2E tests."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self._login_self()
        store = self._create_test_store()
        url = self.live_server_url
        self.url = f"{url}/stores/delete/{store.id}"

    def tearDown(self) -> None:
        """Tear down the test."""
        Store.objects.all().delete()
        return super().tearDown()

    def test_delete_page(self) -> None:
        """Test the delete page."""
        self.driver.get(self.url)
        time.sleep(1)

        self.driver.get_screenshot_as_file("./screenshots/stores/delete_page.png")
        self.driver.find_element(value="submit-delete-store").click()

        current_url = self.driver.current_url
        time.sleep(1)
        self.driver.get_screenshot_as_file("./screenshots/stores/post_delete_page.png")
        self.assertEqual(current_url, f"{self.live_server_url}/stores/me")
