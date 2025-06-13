"""Tests for the error views."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestErrorViews(TestCase):
    """Tests for the error views."""

    def setUp(self) -> None:
        """
        Set up the tests.

        1. Create a test client.
        2. Create a test user.
        3. Force login the test user.
        """
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        return super().setUp()

    def get_url(self, status_code: int) -> str:
        """
        Get the url for the debug status code view.

        Args:
            status_code (int): The status code to debug.

        Returns:
            str: The url for the debug status code view.
        """
        return reverse("debug_status_code", args=[status_code])

    def test_bad_request_view(self) -> None:
        """
        Test the bad request view.

        Given: The user is logged in.
        When: The user submits a request with a bad request exception.
        Then: The user receives a 400 status code and the error page is rendered.
        """
        response = self.client.get(self.get_url(400))
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, "dashboard/err/400.html")

    def test_permission_denied_view(self) -> None:
        """
        Test the permission denied view.

        Given: The user is logged in.
        When: The user submits a request with a permission denied exception.
        Then: The user receives a 403 status code and the error page is rendered.
        """
        response = self.client.get(self.get_url(403))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "dashboard/err/403.html")

    def test_not_found_view(self) -> None:
        """
        Test the not found view.

        Given: The user is logged in.
        When: The user submits a request with a not found exception.
        Then: The user receives a 404 status code and the error page is rendered.
        """
        response = self.client.get(self.get_url(404))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/err/404.html")
