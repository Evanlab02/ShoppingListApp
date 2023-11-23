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
MOCK_PASSWORD = "TestRegister"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Register"

class TestLoginPage(TestCase):
    """Contains end-to-end tests for the register page."""

    def setUp(self) -> None:
        """Set up the test driver."""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )
        self.delay = 3
        return super().setUp()

    def tearDown(self) -> None:
        """Close the test driver."""
        self.driver.close()
        return super().tearDown()

    def test_register(self) -> None:
        """Test that a user can register."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 1")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test1@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()
        
        self.assertEqual(self.driver.current_url, LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 1")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_register_with_only_mandatory_values(self) -> None:
        """Test that a user can register with only mandatory values."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 2")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()
        
        self.assertEqual(self.driver.current_url, LOGIN_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 2")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.assertEqual(self.driver.current_url, DASHBOARD_URL)

    def test_register_with_mismatched_passwords(self) -> None:
        """Test that a user cannot register with mismatched passwords."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 3")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("MismatchedPassword")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()
        
        elementText = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(elementText, "'Passwords do not match.'")

    def test_register_with_existing_username(self) -> None:
        """Test that a user cannot register with an existing username."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 4")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 4")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        elementText = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(elementText, "'Username already exists.'")

    def test_register_with_existing_email(self) -> None:
        """Test that a user cannot register with an existing email."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 5")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("registeruser5@register.com")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 6")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("registeruser5@register.com")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        elementText = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(elementText, "'Email already exists.'")
