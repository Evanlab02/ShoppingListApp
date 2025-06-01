"""Contains tests for the token routes."""

import jwt
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from authentication.tests.factory import ClientFactory, UserFactory

CONTENT_TYPE = "application/json"
SUCCESS_REGISTER_MESSAGE = "User successfully registered."
SUCCESS_LOGIN_MESSAGE = "User successfully logged in."
TEST_EMAIL = "test@login.com"


class TestTokenRouter(TestCase):
    """Tests for the token routes."""

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()
        self.user = UserFactory.create()
        self.api_client = ClientFactory.create(user=self.user)

    def test_token_refresh(self) -> None:
        """Test the token refresh endpoint."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("ninja-api:auth_token"))
        self.assertEqual(response.status_code, 200)

    def test_token_refresh_decodes_correct_token(self) -> None:
        """Test the token refresh endpoint."""
        self.client.force_login(self.user)
        response = self.client.get(reverse("ninja-api:auth_token"))
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        token = response_data["token"]
        secret = response_data["secret"]

        self.api_client.refresh_from_db()

        self.assertEqual(token, self.api_client.token)
        self.assertEqual(secret, self.api_client.client_secret)

        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded_token["username"], self.user.username)
        self.assertEqual(decoded_token["client_id"], self.api_client.id)

    def test_token_refresh_returns_401_if_not_logged_in(self) -> None:
        """Test the token refresh endpoint returns 401 if not logged in."""
        response = self.client.get(reverse("ninja-api:auth_token"))
        self.assertEqual(response.status_code, 401)
