"""Contains tests for the login view."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from authenticationapp.models import Client as ClientModel

TEST_EMAIL = "user@test.com"
FONT = '<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">'
DASHBOARD_ROUTE = "/shopping/dashboard/"
LOGIN_ACTION_ROUTE = "/login/action"


class TestLoginView(TestCase):
    """Test the login view."""

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

    def test_get_login_page(self):
        """Test the login page."""
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/index.html")

    def test_login_action_endpoint_when_logged_in(self):
        """Test the login action endpoint redirects to the dashboard when user is logged in."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(
            LOGIN_ACTION_ROUTE, {"username-input": "", "password-input": ""}
        )
        self.assertRedirects(
            response,
            "/?error='Already logged in.'",
            302,
            404,
            fetch_redirect_response=False,
        )

    def test_login_action_endpoint_when_not_logged_in(self):
        """Test the login action endpoint redirects when the user logs in."""
        response = self.client.post(
            LOGIN_ACTION_ROUTE,
            {"username-input": "testuser", "password-input": "testpassword"},
        )
        self.assertRedirects(
            response, DASHBOARD_ROUTE, 302, 404, fetch_redirect_response=False
        )

    def test_login_action_endpoint_invalid_username(self):
        """Test the login action endpoint redirects to the dashboard when the user is logged in."""
        response = self.client.post(
            LOGIN_ACTION_ROUTE,
            {"username-input": "invalid", "password-input": "testpassword"},
        )
        self.assertRedirects(
            response,
            "/?error='Invalid credentials.'",
            302,
            200,
            fetch_redirect_response=False,
        )
