"""Contains tests for the register view."""
import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.views import DASHBOARD_ROUTE, REGISTER_ROUTE

TEST_EMAIL = "user@test.com"


class TestRegisterView(TestCase):
    """Test the register view."""

    @pytest.mark.django_db(transaction=True)
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

    def test_get_login_page(self) -> None:
        """Test the register page."""
        response = self.client.get(f"/{REGISTER_ROUTE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")

    def test_get_login_page_when_already_logged_in(self) -> None:
        """Test the register page."""
        self.client.force_login(self.user)
        response = self.client.get(f"/{REGISTER_ROUTE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/{DASHBOARD_ROUTE}", 302, 404)
