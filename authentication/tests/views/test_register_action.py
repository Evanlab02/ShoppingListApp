"""Contains tests for the register action view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.constants import INPUT_MAPPING
from authentication.views import (
    DASHBOARD_ROUTE,
    LOGIN_ROUTE,
    REGISTER_ACTION_ROUTE,
    REGISTER_ROUTE,
)

TEST_EMAIL = "user@test.com"
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
EMAIL_INPUT = INPUT_MAPPING.get("email-input", "email-input")
FIRST_NAME_INPUT = INPUT_MAPPING.get("first-name-input", "first-name-input")
LAST_NAME_INPUT = INPUT_MAPPING.get("last-name-input", "last-name-input")
PASSWORD_CONFIRM_INPUT = INPUT_MAPPING.get("password-confirm-input", "password-confirm-input")


class TestRegisterActionView(TestCase):
    """Test the login view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="tester@gmail.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_register_action_endpoint(self) -> None:
        """Test the register action endpoint."""
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}",
            {
                USERNAME_INPUT: "registeruser",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: TEST_EMAIL,
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(response, f"/{LOGIN_ROUTE}", 302, 200, fetch_redirect_response=False)

    def test_register_action_endpoint_when_already_logged_in(self) -> None:
        """Test the register action endpoint redirects when the user is already logged in."""
        self.client.force_login(self.user)
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}",
            {
                USERNAME_INPUT: "registeruser",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: TEST_EMAIL,
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response, f"/{DASHBOARD_ROUTE}", 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_with_invalid_username(self) -> None:
        """Test the register action endpoint with an invalid username."""
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}",
            {
                USERNAME_INPUT: "",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: TEST_EMAIL,
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response,
            f"/{REGISTER_ROUTE}?error=Please ensure username, email, first name and last name are provided.",  # noqa: E501
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_with_invalid_password(self) -> None:
        """Test the register action endpoint with an invalid password."""
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}",
            {
                USERNAME_INPUT: "registeruser",
                PASSWORD_INPUT: "abcd",
                EMAIL_INPUT: TEST_EMAIL,
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response,
            f"/{REGISTER_ROUTE}?error=Password+and+password+confirmation+do+not+match.",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_already_existing_username(self) -> None:
        """Test the register action endpoint with an already existing username."""
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}",
            {
                USERNAME_INPUT: "testuser",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: TEST_EMAIL,
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response,
            f"/{REGISTER_ROUTE}?error=Username+already+exists.",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_already_existing_email(self) -> None:
        """Test the register action endpoint with an already existing email."""
        response = self.client.post(
            f"/{REGISTER_ACTION_ROUTE}?error=Email+already+exists.",
            {
                USERNAME_INPUT: "registeruser",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: "tester@gmail.com",
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response,
            f"/{REGISTER_ROUTE}?error=Email+already+exists.",
            302,
            200,
            fetch_redirect_response=False,
        )
