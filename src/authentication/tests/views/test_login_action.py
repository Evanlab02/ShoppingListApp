"""Contains tests for the login view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.constants import INPUT_MAPPING
from authentication.views import DASHBOARD_ROUTE, LOGIN_ACTION_ROUTE, LOGIN_ROUTE

TEST_EMAIL = "user@test.com"
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")


class TestLoginView(TestCase):
    """Test the login view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email=TEST_EMAIL,
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_login_action_endpoint_when_not_logged_in(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        response = self.client.post(
            f"/{LOGIN_ACTION_ROUTE}",
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "testpassword"},
        )
        self.assertRedirects(
            response, f"/{DASHBOARD_ROUTE}", 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_when_logged_in(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        self.client.force_login(self.user)
        response = self.client.post(
            f"/{LOGIN_ACTION_ROUTE}",
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "testpassword"},
        )
        self.assertRedirects(
            response, f"/{DASHBOARD_ROUTE}", 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_with_invalid_credentials(self) -> None:
        """Test the login action endpoint redirects when the user logs in."""
        response = self.client.post(
            f"/{LOGIN_ACTION_ROUTE}",
            {USERNAME_INPUT: "testuser", PASSWORD_INPUT: "invalidpassword"},
        )
        self.assertRedirects(
            response,
            f"/{LOGIN_ROUTE}?error=Invalid Credentials.",
            302,
            404,
            fetch_redirect_response=False,
        )
