"""Contains end-to-end tests for the register page."""

from unittest import TestCase

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from authentication.constants import INPUT_MAPPING

# Urls
REGISTER_URL = "http://localhost:7001/register"
LOGIN_URL = "http://localhost:7001/"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
CONFIRM_PASSWORD_INPUT = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")
EMAIL_INPUT = INPUT_MAPPING.get("email-input", "email-input")
FIRST_NAME_INPUT = INPUT_MAPPING.get("first-name-input", "first-name-input")
LAST_NAME_INPUT = INPUT_MAPPING.get("last-name-input", "last-name-input")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
ERROR_TEXT = "error-text"

# Mock data
MOCK_PASSWORD = "TestRegister"
MOCK_FIRST_NAME = "Selenium"
MOCK_LAST_NAME = "Register"


class TestRegisterPage(TestCase):
    """Contains end-to-end tests for the register page."""

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

    def test_register_with_mismatched_passwords(self) -> None:
        """Test that a user cannot register with mismatched passwords."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 3")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("MismatchedPassword")
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test3@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Password and password confirmation do not match.")

    def test_register_with_existing_username(self) -> None:
        """Test that a user cannot register with an existing username."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 4")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test4@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 4")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test5@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Username already exists.")

    def test_register_with_existing_email(self) -> None:
        """Test that a user cannot register with an existing email."""
        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 5")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("registeruser5@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get(REGISTER_URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("Register Test User 6")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys(MOCK_PASSWORD)
        self.driver.find_element(value=EMAIL_INPUT).send_keys("registeruser5@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys(MOCK_FIRST_NAME)
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys(MOCK_LAST_NAME)
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Email already exists.")
