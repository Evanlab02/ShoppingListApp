"""Contains the end to end tests for the register view."""

from django.contrib.auth.models import User

from authentication.constants import INPUT_MAPPING
from authentication.tests.E2E.base_test_case import BaseEndToEndTestCase
from authentication.tests.helpers import create_test_user

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
CONFIRM_PASSWORD_INPUT = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")
EMAIL_INPUT = INPUT_MAPPING.get("email-input", "email-input")
FIRST_NAME_INPUT = INPUT_MAPPING.get("first-name-input", "first-name-input")
LAST_NAME_INPUT = INPUT_MAPPING.get("last-name-input", "last-name-input")
SUBMIT_REGISTRATION = INPUT_MAPPING.get("submit-register", "submit-register")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
ERROR_TEXT = "error-text"


class TestRegisterView(BaseEndToEndTestCase):
    """Tests the register view with E2E tests."""

    def setUp(self) -> None:
        """Set up the tests."""
        create_test_user()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_register(self) -> None:
        """Test that a user can register."""
        URL = f"{self.live_server_url}/register"
        TARGET_URL = f"{self.live_server_url}/"

        self.driver.get(URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("new_test_user")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test1@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys("test_name")
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys("test_last_name")
        self.driver.get_screenshot_as_file("./screenshots/register/pre_submit.png")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()
        self.driver.get_screenshot_as_file("./screenshots/register/post_submit.png")
        self.assertEqual(self.driver.current_url, TARGET_URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=SUBMIT_LOGIN).click()

    def test_register_with_mismatched_passwords(self) -> None:
        """Test that a user cannot register with mismatched passwords."""
        URL = f"{self.live_server_url}/register"

        self.driver.get(URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("mismatched_test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("MismatchedPassword")
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test3@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys("test_name")
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys("test_last_name")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get_screenshot_as_file("./screenshots/register/mismatched_passwords.png")
        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Password and password confirmation do not match.")

    def test_register_with_existing_username(self) -> None:
        """Test that a user cannot register with an existing username."""
        URL = f"{self.live_server_url}/register"

        self.driver.get(URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test5@register.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys("test")
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys("test_last_name")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get_screenshot_as_file("./screenshots/register/existing_username.png")
        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Username already exists.")

    def test_register_with_existing_email(self) -> None:
        """Test that a user cannot register with an existing email."""
        URL = f"{self.live_server_url}/register"

        self.driver.get(URL)
        self.driver.find_element(value=USERNAME_INPUT).send_keys("new_test_user")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=CONFIRM_PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=EMAIL_INPUT).send_keys("test@gmail.com")
        self.driver.find_element(value=FIRST_NAME_INPUT).send_keys("test")
        self.driver.find_element(value=LAST_NAME_INPUT).send_keys("test_last_name")
        self.driver.find_element(value=SUBMIT_REGISTRATION).click()

        self.driver.get_screenshot_as_file("./screenshots/register/existing_email.png")
        element_text = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(element_text, "Email already exists.")
