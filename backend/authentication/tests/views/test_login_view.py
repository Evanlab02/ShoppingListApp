"""Contains tests for the login view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLoginView(TestCase):
    """Test the login view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_get_login_page(self) -> None:
        """Test the login page."""
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/index.html")

    def test_get_login_page_when_already_logged_in(self) -> None:
        """Test the login page."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"), 302, 200)
