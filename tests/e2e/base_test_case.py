"""Contains the BaseTestCase class for end-to-end tests."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING

# Urls
LOGIN_URL = "http://localhost:7001/"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")

# Mock data
MOCK_USERNAME = "basetestuser1"
MOCK_PASSWORD = "testuser"


class BaseTestCase(TestCase):
    """Contains the BaseTestCase class for end-to-end tests."""

    driver: webdriver.Chrome
    delay: int
    mock_username: str
    mock_password: str

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # type: ignore
        options.add_argument("--start-maximized")  # type: ignore
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.driver.set_window_size(1920, 1080, cls.driver.window_handles[0])

        cls.delay = 3
        cls.mock_username = MOCK_USERNAME
        cls.mock_password = MOCK_PASSWORD

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()

    def _login(self) -> None:
        """Log in to the site."""
        self.driver.get(LOGIN_URL)

        if self.driver.current_url == DASHBOARD_URL:
            return

        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)
