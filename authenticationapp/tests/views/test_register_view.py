"""Contains tests for the register view."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from authenticationapp.models import Client as ClientModel

TEST_EMAIL = "user@test.com"
FONT = '<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">'
REGISTER_ACTION_ROUTE = "/register/action"
DASHBOARD_ROUTE = "/shopping/dashboard/"
USERNAME_ERROR_ROUTE = "/register/error/username-already-exists"


class TestRegisterView(TestCase):
    """Test the register view."""

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

    def test_get_register_page(self):
        """Should render the register page."""
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth/register.html")

    def test_register_action_when_logged_in(self):
        """Should redirect to the dashboard."""
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(REGISTER_ACTION_ROUTE)
        self.assertRedirects(
            response,
            "/?error='Already logged in.'",
            302,
            404,
            fetch_redirect_response=False,
        )

    def test_register_action_valid_credentials(self):
        """Should redirect to the dashboard."""
        response = self.client.post(
            REGISTER_ACTION_ROUTE,
            {
                "username-input": "newuser",
                "password-input": "newpassword",
                "confirm-password-input": "newpassword",
                "email-input": "test@test2.com",
                "first-name-input": "new",
                "last-name-input": "user",
            },
        )

        self.assertRedirects(response, "/", 302, 200, fetch_redirect_response=False)

    def test_register_action_invalid_username(self):
        """Should redirect to the register page."""
        response = self.client.post(
            REGISTER_ACTION_ROUTE,
            {
                "username-input": "testuser",
                "password-input": "newpassword",
                "confirm-password-input": "newpassword",
                "email-input": "tester@test.com",
                "first-name-input": "new",
                "last-name-input": "user",
            },
        )

        self.assertRedirects(
            response,
            "/register?error='Username already exists.'",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_register_action_invalid_email(self):
        """Should redirect to the register page."""
        response = self.client.post(
            REGISTER_ACTION_ROUTE,
            {
                "username-input": "newuser",
                "password-input": "newpassword",
                "confirm-password-input": "newpassword",
                "email-input": TEST_EMAIL,
                "first-name-input": "new",
                "last-name-input": "user",
            },
        )

        self.assertRedirects(
            response,
            "/register?error='Email already exists.'",
            302,
            200,
            fetch_redirect_response=False,
        )

    def test_register_action_invalid_passwords(self):
        """Should redirect to the register page."""
        response = self.client.post(
            REGISTER_ACTION_ROUTE,
            {
                "username-input": "newuser",
                "password-input": "newpassword",
                "confirm-password-input": "newpassword2",
                "email-input": "tester@gmail.com",
                "first-name-input": "new",
                "last-name-input": "user",
            },
        )

        self.assertRedirects(
            response,
            "/register?error='Passwords do not match.'",
            302,
            200,
            fetch_redirect_response=False,
        )
