"""Contains tests for the logout view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLogoutView(TestCase):
    """Test the logout view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_logout_page(self) -> None:
        """Test the logout page."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")

    def test_logout_page_when_not_logged_in(self) -> None:
        """Test the logout page."""
        response = self.client.get(reverse("logout_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login_page") + "?error=You must be logged in to access that page.",
            302,
            200,
        )
