"""Contains tests for the register action view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.constants import INPUT_MAPPING
from authentication.tests.factory import UserFactory
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
        self.user = UserFactory()

    def test_register_action_endpoint(self) -> None:
        """Test the register action endpoint."""
        response = self.client.post(
            reverse("register_action"),
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
            response, reverse("login_page"), 302, 200, fetch_redirect_response=False
        )

    def test_register_action_endpoint_when_already_logged_in(self) -> None:
        """Test the register action endpoint redirects when the user is already logged in."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("register_action"),
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
            response, reverse("dashboard"), 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_with_invalid_username(self) -> None:
        """Test the register action endpoint with an invalid username."""
        response = self.client.post(
            reverse("register_action"),
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
            reverse("register_page")
            + "?error=Please ensure username, email, first name and last name are provided.",  # noqa: E501
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_with_invalid_password(self) -> None:
        """Test the register action endpoint with an invalid password."""
        response = self.client.post(
            reverse("register_action"),
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
            reverse("register_page") + "?error=Password and password confirmation do not match.",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_already_existing_username(self) -> None:
        """Test the register action endpoint with an already existing username."""
        UserFactory(username="testuser")
        response = self.client.post(
            reverse("register_action"),
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
            reverse("register_page") + "?error=Username already exists.",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_already_existing_email(self) -> None:
        """Test the register action endpoint with an already existing email."""
        UserFactory(username="random_very_random_username", email="duplicate@gmail.com")
        response = self.client.post(
            reverse("register_action"),
            {
                USERNAME_INPUT: "registeruser",
                PASSWORD_INPUT: "testpassword",
                EMAIL_INPUT: "duplicate@gmail.com",
                FIRST_NAME_INPUT: "test",
                LAST_NAME_INPUT: "user",
                PASSWORD_CONFIRM_INPUT: "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("register_page") + "?error=Email already exists.",
            302,
            200,
            fetch_redirect_response=False,
        )
