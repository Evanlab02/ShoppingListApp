"""Contains end-to-end tests for the register page."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Urls
REGISTER_URL = "http://localhost:7001/register"
LOGIN_URL = "http://localhost:7001/"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
USERNAME_INPUT = "username-input"
PASSWORD_INPUT = "password-input"
CONFIRM_PASSWORD_INPUT = "confirm-password-input"
EMAIL_INPUT = "email-input"
FIRST_NAME_INPUT = "first-name-input"
LAST_NAME_INPUT = "last-name-input"
SUBMIT_REGISTRATION = "submit-registration"
SUBMIT_LOGIN = "submit-login"
ERROR_TEXT = "error-text"

# Mock data
MOCK_USERNAME = "Login Test User"
MOCK_PASSWORD = "TestLogin"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Login"
MOCK_EMAIL = "testlogin@selenium.com"


class TestLoginPage(TestCase):
    """Contains end-to-end tests for the login page."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=options
        )
        cls.delay = 3

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the test driver."""
        cls.driver.close()

    def test_1_register(self) -> None:
        """Test that a user can register."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys(MOCK_EMAIL)
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

    def test_2_login(self) -> None:
        self.driver.get(LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys(MOCK_USERNAME)
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)
