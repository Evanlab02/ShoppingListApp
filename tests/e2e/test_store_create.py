"""
Contains end-to-end tests for the store create page.
"""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

STORE_CREATE_URL = "http://localhost:7001/stores/create"
LOGIN_URL = "http://localhost:7001/"


class TestStoreCreatePage(TestCase):
    """Contains end-to-end tests for the store create page."""

    def setUp(self) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # type: ignore
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        self.delay = 3
        return super().setUp()

    def tearDown(self) -> None:
        """Close the test driver."""
        self.driver.close()
        return super().tearDown()

    def test_get_create_page_without_being_logged_in(self) -> None:
        """Test that a user cannot access the create store page without being logged in."""
        self.driver.get(STORE_CREATE_URL)
        self.assertEqual(self.driver.current_url, f"{LOGIN_URL}?next=/stores/create")
