"""Contains the tests for the dashboard views."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestDashboard(TestCase):
    """Test the dashboard views."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)

    def test_dashboard_overview(self) -> None:
        """Test the dashboard overview."""
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")
