"""Contains the login API tests."""

from authentication.tests.api.base_test_case import BaseTestCase


class LoginAPITests(BaseTestCase):
    """Login api tests."""

    def test_login(self) -> None:
        """Test that a user can login."""
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": self.user.username,
            "password": "test",
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")
        self.assertEqual(response.json()["detail"], "")

    def test_login_again_when_already_logged_in(self) -> None:
        """Test that a user cannot login again when already logged in."""
        self.client.force_login(self.user)
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": self.user.username,
            "password": "test",
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already logged in.")

    def test_login_with_invalid_credentials(self) -> None:
        """Test that a user cannot login with invalid credentials."""
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": self.user.username,
            "password": "invalid",
        }
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Invalid Credentials.")
