"""Contains tests for the login view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.constants import INPUT_MAPPING
from authentication.tests.factory import UserFactory
from authentication.views import DASHBOARD_ROUTE, LOGIN_ACTION_ROUTE, LOGIN_ROUTE

USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")


class TestLoginView(TestCase):
    """Test the login view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory(username="testuser")

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_login_action_endpoint_when_not_logged_in(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        response = self.client.post(
            reverse("login_action"),
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "test"},
        )
        self.assertRedirects(
            response, reverse("dashboard"), 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_when_logged_in(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("login_action"),
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "test"},
        )
        self.assertRedirects(
            response, reverse("dashboard"), 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_with_invalid_credentials(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        response = self.client.post(
            reverse("login_action"),
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "invalidpassword"},
        )
        self.assertRedirects(
            response,
            f"/{LOGIN_ROUTE}?error=Invalid Credentials.",
            302,
            404,
            fetch_redirect_response=False,
        )
