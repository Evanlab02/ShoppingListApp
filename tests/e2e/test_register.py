"""Contains end-to-end tests for the register page."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


class TestLoginPage(TestCase):
    """Contains end-to-end tests for the register page."""

    def setUp(self) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        self.delay = 3
        return super().setUp()

    def tearDown(self) -> None:
        """Close the test driver."""
        self.driver.close()
        return super().tearDown()

    def test_register(self) -> None:
        """Test that a user can register."""
        self.driver.get("http://localhost:7001/register")
        self.driver.find_element(value="username-input").send_keys("Selenium Test User")
        self.driver.find_element(value="password-input").send_keys("TestPass")
        self.driver.find_element(value="confirm-password-input").send_keys("TestPass")
        self.driver.find_element(value="email-input").send_keys("test@test.com")
        self.driver.find_element(value="first-name-input").send_keys("Selenium")
        self.driver.find_element(value="last-name-input").send_keys("Test")
        self.driver.find_element(value="submit-registration").click()
        self.assertEqual(self.driver.current_url, "http://localhost:7001/")
