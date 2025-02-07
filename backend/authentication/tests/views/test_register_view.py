"""Contains tests for the register view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from authentication.views import DASHBOARD_ROUTE, REGISTER_ROUTE

TEST_EMAIL = "user@test.com"


class TestRegisterView(TestCase):
    """Test the register view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_get_register_page(self) -> None:
        """Test the register page."""
        response = self.client.get(reverse("register_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")

    def test_get_register_page_when_already_logged_in(self) -> None:
        """Test the register page when the user is already logged in."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("register_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"), 302, 200)
