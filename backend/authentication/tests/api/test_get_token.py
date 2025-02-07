"""Contains the token API tests."""

import jwt

from authentication.models import ApiClient
from authentication.tests.api.base_test_case import BaseTestCase


class TokenAPITests(BaseTestCase):
    """Token api tests."""

    def test_get_token(self) -> None:
        """Test that a user can get a token."""
        self.client.force_login(self.user)
        url = f"{self.live_server_url}/api/v1/token"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        token = response.json()["token"]
        secret = response.json()["secret"]

        api_client = ApiClient.objects.get(user=self.user)
        self.assertEqual(api_client.token, token)
        self.assertEqual(api_client.client_secret, secret)

        decoded_token = jwt.decode(token, secret, algorithms=["HS256"])
        self.assertEqual(decoded_token["username"], self.user.username)
        self.assertEqual(decoded_token["client_id"], api_client.id)
