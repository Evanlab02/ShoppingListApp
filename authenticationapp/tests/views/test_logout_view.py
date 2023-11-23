"""Contains tests for the logout view."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from authenticationapp.models import Client as ClientModel

TEST_EMAIL = "user@test.com"
FONT = '<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">'


class TestLogoutView(TestCase):
    """Test the logout view."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self):
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

        self.client_model = ClientModel.objects.create(user=self.user)

    def test_logout_action(self):
        """Test the logout action."""
        self.client.force_login(self.user)
        response = self.client.post("/logout/action")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_logout_action_redirects_if_not_logged_in(self):
        """Test the logout action redirects if the user is not logged in."""
        response = self.client.post("/logout/action")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_get_logout_page(self):
        """Test the logout page."""
        self.client.force_login(self.user)
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 200)

    def test_get_logout_page_redirects_if_not_logged_in(self):
        """Test the logout page redirects if the user is not logged in."""
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=False,
        )
        self.assertFalse(response.wsgi_request.user.is_authenticated)
