"""Contains the logout API tests."""

from authentication.tests.api.base_test_case import BaseTestCase


class LogoutAPITests(BaseTestCase):
    """Logout api tests."""

    def test_logout(self) -> None:
        """Test that a user can logout."""
        self.client.force_login(self.user)
        url = f"{self.live_server_url}/api/v1/auth/logout"
        response = self.client.post(url, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged out.")

    def test_can_not_logout_when_not_logged_in(self) -> None:
        """Test that a user cannot logout when not logged in."""
        url = f"{self.live_server_url}/api/v1/auth/logout"
        response = self.client.post(url, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is not logged in.")
