"""Contains the tests for the dashboard views."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestDashboard(TestCase):
    """
    Test the dashboard views.

    Tests: dashboard.views.dashboard
    """

    def setUp(self) -> None:
        """Set up the tests.

        1. Create a test user.
        2. Setup the test client.
        3. Force login the test user.
        4. Call the super setup method.
        """
        self.user = UserFactory.create()
        self.client = Client()
        self.client.force_login(self.user)
        return super().setUp()

    def test_dashboard_overview(self) -> None:
        """
        Test the dashboard overview.

        Given: The user is logged in.
        When: The user visits the dashboard.
        Then: The user receives a 200 status code and is shown the dashboard.
        """
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/index.html")

    def test_dashboard_overview_when_not_logged_in(self) -> None:
        """
        Test the dashboard overview when the user is not logged in.

        Given: The user is not logged in.
        When: The user visits the dashboard.
        Then: The user is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login_page')}?error=You must be logged in to access that page.",
            302,
            200,
        )

    def test_dashboard_overview_with_post_request(self) -> None:
        """
        Test the dashboard overview with a post request.

        Given: The user is logged in.
        When: The user visits the dashboard using a post request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.post(reverse("dashboard"))
        self.assertEqual(response.status_code, 405)
