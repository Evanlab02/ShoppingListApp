"""Base router test case."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class BaseRouterTestCase(TestCase):
    """Base router test case."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.content_type = "application/json"
        self.user = UserFactory.create()

        self.client = Client()

        self.token_url = reverse("ninja-api:auth_token")
        self.client.force_login(self.user)
        self.token_response = self.client.get(self.token_url, content_type=self.content_type)
        self.token = self.token_response.json()["token"]
        self.secret = self.token_response.json()["secret"]

        self.base_headers = {"X-API-Token": self.token}
