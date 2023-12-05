"""Contains tests for the login view."""

from django.test import TestCase


class TestLoginView(TestCase):
    """Test the login view."""

    def test_get_login_page(self) -> None:
        """Test the login page."""
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/index.html")
