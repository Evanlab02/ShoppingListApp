"""Tests the logout action."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLogoutAction(TestCase):
    """Test the logout action route."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_logout_action(self) -> None:
        """Test the logout action."""
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"), 302, 200)

    def test_logout_action_not_logged_in(self) -> None:
        """Test the logout action when not logged in."""
        response = self.client.post(reverse("logout_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("login_page") + "?error=You must be logged in to access that page.",
            302,
            200,
        )
