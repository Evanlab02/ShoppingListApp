"""Contains the end to end tests for the login view."""

from django.contrib.auth.models import User

from authentication.constants import INPUT_MAPPING
from authentication.tests.E2E.base_test_case import BaseEndToEndTestCase
from authentication.tests.helpers import create_test_user

# Element IDs
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")


class TestLoginView(BaseEndToEndTestCase):
    """Tests the login view with E2E tests."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        return super().tearDown()

    def test_login(self) -> None:
        """Test the login view."""
        URL = self.live_server_url
        TARGET_URL = f"{self.live_server_url}/shopping/dashboard/"
        self.driver.get(URL)

        self.driver.find_element(value=USERNAME_INPUT).send_keys("test")
        self.driver.find_element(value=PASSWORD_INPUT).send_keys("test")

        self.driver.get_screenshot_as_file("./screenshots/login/login_pre_submit.png")

        self.driver.find_element(value=SUBMIT_LOGIN).click()

        self.driver.get_screenshot_as_file("./screenshots/login/login_post_submit.png")

        self.assertEqual(self.driver.current_url, TARGET_URL)
