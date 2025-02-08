"""Contains the end to end tests for the login view."""

import time

from django.contrib.auth.models import User
from django.urls import reverse

from authentication.constants import INPUT_MAPPING
from authentication.tests.E2E.base_test_case import BaseEndToEndTestCase
from authentication.tests.factory import UserFactory

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")


class TestLoginView(BaseEndToEndTestCase):
    """Tests the login view with E2E tests."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_user_can_view_login_page(self) -> None:
        """Test the login view."""
        URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)
        self.driver.get_screenshot_as_file("./screenshots/login/test_user_can_view_login_page.png")

    def test_login_page_has_correct_heading(self) -> None:
        """Test the login page has the correct heading."""
        URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        heading = self.driver.find_element(value="auth-heading").text
        self.assertEqual(heading, "Shopping App Login")

    def test_login_page_can_render_error_message(self) -> None:
        """Test the login page can render an error message."""
        error = "This a test error messsage, please ignore."
        URL = f"{self.live_server_url}{reverse('login_page')}?error={error}"

        self.driver.get(URL)

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, error)
        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_login_page_can_render_error_message.png"
        )

    def test_login_form_has_correct_url(self) -> None:
        """Test the login form has the correct URL."""
        URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        login_form = self.driver.find_element(value="login-form")
        login_form_url = login_form.get_attribute("action")
        self.assertEqual(login_form_url, f"{self.live_server_url}{reverse('login_action')}")

    def test_login_page_can_fill_in_inputs(self) -> None:
        """Test the login page can fill in the inputs."""
        URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys(self.user.username)
        username_input_value = username_input.get_attribute("value")
        self.assertEqual(username_input_value, self.user.username)

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")
        password_input_value = password_input.get_attribute("value")
        self.assertEqual(password_input_value, "test")

        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_login_page_can_fill_in_inputs.png"
        )

    def test_login_page_can_go_to_register_page(self) -> None:
        """Test the login page can go to the register page."""
        URL = f"{self.live_server_url}{reverse('login_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('register_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        register_button = self.driver.find_element(value="go-to-register")
        register_button.click()
        self.assertEqual(self.driver.current_url, TARGET_URL)
        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_login_page_can_go_to_register_page.png"
        )

    def test_login_page_can_submit_form(self) -> None:
        """Test the login page can submit the form."""
        URL = f"{self.live_server_url}{reverse('login_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('dashboard')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys(self.user.username)

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("test")

        submit_button = self.driver.find_element(value=SUBMIT_LOGIN)
        submit_button.click()

        self.assertEqual(self.driver.current_url, TARGET_URL)
        time.sleep(1)
        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_login_page_can_submit_form.png"
        )

    def test_redirect_to_dashboard_when_logged_in(self) -> None:
        """Test that a user is redirected to the dashboard when logged in."""
        URL = f"{self.live_server_url}{reverse('login_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('dashboard')}"

        self.login(self.user.username, "test")

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, TARGET_URL)
        time.sleep(1)
        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_redirect_to_dashboard_when_logged_in.png"
        )

    def test_login_with_invalid_credentials(self) -> None:
        """Test that a user is redirected to the login page with invalid credentials."""
        URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        username_input = self.driver.find_element(value=USERNAME_INPUT)
        username_input.send_keys(self.user.username)

        password_input = self.driver.find_element(value=PASSWORD_INPUT)
        password_input.send_keys("invalid")

        submit_button = self.driver.find_element(value=SUBMIT_LOGIN)
        submit_button.click()

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, "Invalid Credentials.")
        self.driver.get_screenshot_as_file(
            "./screenshots/login/test_login_with_invalid_credentials.png"
        )
