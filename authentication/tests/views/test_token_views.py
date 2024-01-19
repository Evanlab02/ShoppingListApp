"""Contains tests for the login view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.views import (
    CONFIRM_TOKEN_ROUTE,
    DISABLE_CLIENT_ROUTE,
    ENABLE_CLIENT_ROUTE,
)

TEST_EMAIL = "user@test.com"


class TestTokenView(TestCase):
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
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_get_confirm_token_page(self) -> None:
        """Test the confirm token page."""
        response = self.client.get(f"/{CONFIRM_TOKEN_ROUTE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/confirm_token.html")

    def test_get_enable_client_page(self) -> None:
        """Test the enable client page."""
        self.client.force_login(self.user)
        response = self.client.get(f"/{ENABLE_CLIENT_ROUTE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/token.html")

    def test_get_disable_client_page(self) -> None:
        """Test the disable client page."""
        self.client.force_login(self.user)
        response = self.client.get(f"/{DISABLE_CLIENT_ROUTE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/disable-token.html")
