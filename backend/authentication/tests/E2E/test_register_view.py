"""Contains the end to end tests for the register view."""

from django.urls import reverse
import pytest
from django.contrib.auth.models import User

from authentication.constants import INPUT_MAPPING
from authentication.tests.E2E.base_test_case import BaseEndToEndTestCase
from authentication.tests.factory import UserFactory

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
        self.user = UserFactory()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_user_can_view_register_page(self) -> None:
        """Test that a user can view the register page."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)
        self.driver.get_screenshot_as_file("./screenshots/register/test_user_can_view_register_page.png")

    def test_register_page_has_correct_heading(self) -> None:
        """Test that the register page has the correct heading."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        heading = self.driver.find_element(value="auth-heading").text
        self.assertEqual(heading, "Shopping App Register")

    def test_register_page_can_render_error_message(self) -> None:
        """Test that the register page can render an error message."""
        URL = f"{self.live_server_url}{reverse('register_page')}?error=This a test error messsage, please ignore."

        self.driver.get(URL)

        error_message = self.driver.find_element(value=ERROR_TEXT).text
        self.assertEqual(error_message, "This a test error messsage, please ignore.")
        self.driver.get_screenshot_as_file("./screenshots/register/test_register_page_can_render_error_message.png")

    def test_register_form_has_correct_url(self) -> None:
        """Test that the register form has the correct URL."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        register_form = self.driver.find_element(value="register-form")
        register_form_url = register_form.get_attribute("action")
        self.assertEqual(register_form_url, f"{self.live_server_url}{reverse('register_action')}")

    def test_register_page_can_fill_in_inputs(self) -> None:
        """Test that the register page can fill in the inputs."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys("test_user")
        username_input_value = username_input.get_attribute("value")
        self.assertEqual(username_input_value, "test_user")

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")
        password_input_value = password_input.get_attribute("value")
        self.assertEqual(password_input_value, "test")

        confirm_password_input = self.driver.find_element(value=CONFIRM_PASSWORD_INPUT)
        confirm_password_input.send_keys("test")
        confirm_password_input_value = confirm_password_input.get_attribute("value")
        self.assertEqual(confirm_password_input_value, "test")

        email_input = self.driver.find_element(value=EMAIL_INPUT)
        email_input.send_keys("test@register.com")
        email_input_value = email_input.get_attribute("value")
        self.assertEqual(email_input_value, "test@register.com")

        first_name_input = self.driver.find_element(value=FIRST_NAME_INPUT)
        first_name_input.send_keys("test_name")
        first_name_input_value = first_name_input.get_attribute("value")
        self.assertEqual(first_name_input_value, "test_name")

        last_name_input = self.driver.find_element(value=LAST_NAME_INPUT)
        last_name_input.send_keys("test_last_name")
        last_name_input_value = last_name_input.get_attribute("value")
        self.assertEqual(last_name_input_value, "test_last_name")

        self.driver.get_screenshot_as_file("./screenshots/register/test_register_page_can_fill_in_inputs.png")

    def test_register_page_can_submit_form(self) -> None:
        """Test that the register page can submit the form."""
        URL = f"{self.live_server_url}{reverse('register_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys("test_user")

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")

        confirm_password_input = self.driver.find_element(value=CONFIRM_PASSWORD_INPUT)
        confirm_password_input.send_keys("test")

        email_input = self.driver.find_element(value=EMAIL_INPUT)
        email_input.send_keys("test@register.com")

        first_name_input = self.driver.find_element(value=FIRST_NAME_INPUT)
        first_name_input.send_keys("test_name")

        last_name_input = self.driver.find_element(value=LAST_NAME_INPUT)
        last_name_input.send_keys("test_last_name")

        submit_button = self.driver.find_element(value=SUBMIT_REGISTRATION)
        submit_button.click()

        self.assertEqual(self.driver.current_url, TARGET_URL)
        self.driver.get_screenshot_as_file("./screenshots/register/test_register_page_can_submit_form.png")

    def test_register_with_existing_username(self) -> None:
        """Test that a user is redirected to the register page with an existing username."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys(self.user.username)

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")

        confirm_password_input = self.driver.find_element(value=CONFIRM_PASSWORD_INPUT)
        confirm_password_input.send_keys("test")

        email_input = self.driver.find_element(value=EMAIL_INPUT)
        email_input.send_keys("test@register.com")

        first_name_input = self.driver.find_element(value=FIRST_NAME_INPUT)
        first_name_input.send_keys("test_name")

        last_name_input = self.driver.find_element(value=LAST_NAME_INPUT)
        last_name_input.send_keys("test_last_name")

        submit_button = self.driver.find_element(value=SUBMIT_REGISTRATION)
        submit_button.click()

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, "Username already exists.")
        self.driver.get_screenshot_as_file("./screenshots/register/test_register_with_existing_username.png")

    def test_register_with_existing_email(self) -> None:
        """Test that a user is redirected to the register page with an existing email."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys("test_user")

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")

        confirm_password_input = self.driver.find_element(value=CONFIRM_PASSWORD_INPUT)
        confirm_password_input.send_keys("test")

        email_input = self.driver.find_element(value=EMAIL_INPUT)
        email_input.send_keys(self.user.email)

        first_name_input = self.driver.find_element(value=FIRST_NAME_INPUT)
        first_name_input.send_keys("test_name")

        last_name_input = self.driver.find_element(value=LAST_NAME_INPUT)
        last_name_input.send_keys("test_last_name")

        submit_button = self.driver.find_element(value=SUBMIT_REGISTRATION)
        submit_button.click()

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, "Email already exists.")
        self.driver.get_screenshot_as_file("./screenshots/register/test_register_with_existing_email.png")

    def test_register_with_non_matching_passwords(self) -> None:
        """Test that a user is redirected to the register page with non-matching passwords."""
        URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys("test_user")

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")

        confirm_password_input = self.driver.find_element(value=CONFIRM_PASSWORD_INPUT)
        confirm_password_input.send_keys("test_wrong")

        email_input = self.driver.find_element(value=EMAIL_INPUT)
        email_input.send_keys("test@register.com")

        first_name_input = self.driver.find_element(value=FIRST_NAME_INPUT)
        first_name_input.send_keys("test_name")

        last_name_input = self.driver.find_element(value=LAST_NAME_INPUT)
        last_name_input.send_keys("test_last_name")

        submit_button = self.driver.find_element(value=SUBMIT_REGISTRATION)
        submit_button.click()

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, "Password and password confirmation do not match.")
        self.driver.get_screenshot_as_file("./screenshots/register/test_register_with_non_matching_passwords.png")
