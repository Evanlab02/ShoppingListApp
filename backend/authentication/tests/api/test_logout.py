"""Contains the logout API tests."""

from authentication.tests.api.base_test_case import BaseTestCase


class LogoutAPITests(BaseTestCase):
    """Logout api tests."""

    def test_logout(self) -> None:
        """Test that a user can logout."""
        self._login()
        url = f"{self.live_server_url}/api/v1/auth/logout"
        response = self.session.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged out.")

    def test_logout_again(self) -> None:
        """Test that a user cannot logout when not logged in."""
        url = f"{self.live_server_url}/api/v1/auth/logout"
        response = self.session.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is not logged in.")
