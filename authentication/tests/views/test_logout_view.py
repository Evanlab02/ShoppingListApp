"""Contains tests for the logout view."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.views import LOGIN_ROUTE, LOGOUT_ROUTE

TEST_EMAIL = "test_logout@gmail.com"


class TestLogoutView(TestCase):
    """Test the logout view."""

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

    def test_logout_page(self) -> None:
        """Test the logout page."""
        self.client.force_login(self.user)
        response = self.client.get(f"/{LOGOUT_ROUTE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/logout.html")

    def test_logout_page_when_not_logged_in(self) -> None:
        """Test the logout page."""
        response = self.client.get(f"/{LOGOUT_ROUTE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"/{LOGIN_ROUTE}?error=You+must+be+logged+in+to+access+that+page.",
            302,
            200,
        )
