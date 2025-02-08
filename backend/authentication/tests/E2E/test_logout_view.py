"""Contains the end to end tests for the logout view."""

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
SUBMIT_CANCEL_LOGOUT = INPUT_MAPPING.get("submit-cancel", "submit-cancel")
SUBMIT_LOGOUT = INPUT_MAPPING.get("submit-logout", "submit-logout")


class TestLogoutView(BaseEndToEndTestCase):
    """Tests the logout view with E2E tests."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_user_can_view_logout_page(self) -> None:
        """Test user can view logout page."""
        self.login(self.user.username, "test")

        URL = f"{self.live_server_url}{reverse('logout_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)
        self.driver.get_screenshot_as_file(
            "./screenshots/logout/test_user_can_view_logout_page.png"
        )

    def test_logout_page_has_correct_heading(self) -> None:
        """Test logout page has correct heading."""
        self.login(self.user.username, "test")

        URL = f"{self.live_server_url}{reverse('logout_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        heading = self.driver.find_element(value="auth-heading").text
        self.assertEqual(heading, "Shopping App Logout")

    def test_logout_page_can_render_error_message(self) -> None:
        """Test logout page can render error message."""
        self.login(self.user.username, "test")

        error = "This a test error messsage, please ignore."
        URL = f"{self.live_server_url}{reverse('logout_page')}?error={error}"

        self.driver.get(URL)

        error_message = self.driver.find_element(value="error-text").text
        self.assertEqual(error_message, error)
        self.driver.get_screenshot_as_file(
            "./screenshots/logout/test_logout_page_can_render_error_message.png"
        )

    def test_logout_form_has_correct_url(self) -> None:
        """Test logout form has correct URL."""
        self.login(self.user.username, "test")

        URL = f"{self.live_server_url}{reverse('logout_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        logout_form = self.driver.find_element(value="logout-form")
        logout_form_url = logout_form.get_attribute("action")
        self.assertEqual(logout_form_url, f"{self.live_server_url}{reverse('logout_action')}")

    def test_logout_cancel_redirects_to_dashboard(self) -> None:
        """Test logout cancel redirects to dashboard."""
        self.login(self.user.username, "test")

        URL = f"{self.live_server_url}{reverse('logout_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('dashboard')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        submit_button = self.driver.find_element(value=SUBMIT_CANCEL_LOGOUT)
        submit_button.click()
        self.assertEqual(self.driver.current_url, TARGET_URL)
        time.sleep(1)
        self.driver.get_screenshot_as_file(
            "./screenshots/logout/test_logout_cancel_redirects_to_dashboard.png"
        )

    def test_logout_submit_redirects_to_login(self) -> None:
        """Test logout submit redirects to login."""
        self.login(self.user.username, "test")

        URL = f"{self.live_server_url}{reverse('logout_page')}"
        TARGET_URL = f"{self.live_server_url}{reverse('login_page')}"

        self.driver.get(URL)
        self.assertEqual(self.driver.current_url, URL)

        submit_button = self.driver.find_element(value=SUBMIT_LOGOUT)
        submit_button.click()
        self.assertEqual(self.driver.current_url, TARGET_URL)
        self.driver.get_screenshot_as_file(
            "./screenshots/logout/test_logout_submit_redirects_to_login.png"
        )
