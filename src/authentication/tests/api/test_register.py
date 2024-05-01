"""Contains the register API tests."""

from authentication.tests.api.base_test_case import BaseTestCase


class RegisterAPITests(BaseTestCase):
    """Register api tests."""

    def test_register(self) -> None:
        """Test that a user can register."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
            "password_confirmation": "AuthTester1",
            "email": "AuthTester1@gmail.com",
            "first_name": "Auth",
            "last_name": "Tester",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User successfully registered.")
        self.assertEqual(response.json()["detail"], "")

    def test_register_when_logged_in(self) -> None:
        """Test that a user cannot register when logged in."""
        self._login()
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
            "password_confirmation": "AuthTester1",
            "email": "AuthTester1@gmail.com",
            "first_name": "Auth",
            "last_name": "Tester",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already logged in.")
