"""Contains the login API tests."""

from authentication.tests.api.base_test_case import BaseTestCase


class LoginAPITests(BaseTestCase):
    """Login api tests."""

    def test_login(self) -> None:
        """Test that a user can login."""
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": "test",
            "password": "test",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")
        self.assertEqual(response.json()["detail"], "")

    def test_login_again(self) -> None:
        """Test that a user cannot login again."""
        self._login()
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": "test",
            "password": "test",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already logged in.")
