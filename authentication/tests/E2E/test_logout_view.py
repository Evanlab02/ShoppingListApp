"""Contains the end to end tests for the logout view."""

from django.contrib.auth.models import User

from authentication.constants import INPUT_MAPPING
from authentication.tests.E2E.base_test_case import BaseEndToEndTestCase
from authentication.tests.helpers import create_test_user

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
        create_test_user()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_1_logout_cancel(self) -> None:
        """Test logout cancelling."""
        self.driver.get(f"{self.live_server_url}/")
        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=SUBMIT_LOGIN).click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/shopping/dashboard/")

        URL = f"{self.live_server_url}/logout"

        self.driver.get(URL)
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_1.png")
        self.driver.find_element(value=SUBMIT_CANCEL_LOGOUT).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_cancel.png")
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/shopping/dashboard/")

    def test_2_logout(self) -> None:
        """Test logout."""
        self.driver.get(f"{self.live_server_url}/")
        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")
        self.driver.find_element(value=SUBMIT_LOGIN).click()
        self.assertEqual(self.driver.current_url, f"{self.live_server_url}/shopping/dashboard/")

        URL = f"{self.live_server_url}/logout"
        TARGET_URL = self.live_server_url

        self.driver.get(URL)
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_2.png")
        self.driver.find_element(value=SUBMIT_LOGOUT).click()
        self.driver.get_screenshot_as_file("./screenshots/logout/logout_submit.png")
        self.assertEqual(self.driver.current_url, f"{TARGET_URL}/")
