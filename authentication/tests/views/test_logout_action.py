from django.contrib.auth.models import User
from django.test import Client, TestCase

from authentication.views import LOGIN_ROUTE, LOGOUT_ACTION_ROUTE

TEST_EMAIL = "test_logout_action@gmail.com"


class TestLogoutAction(TestCase):
    """Test the logout action route."""

    def setUp(self) -> None:
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
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_logout_action(self) -> None:
        """Test the logout action."""
        self.client.force_login(self.user)
        response = self.client.post(f"/{LOGOUT_ACTION_ROUTE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/{LOGIN_ROUTE}", 302, 200)

    def test_logout_action_not_logged_in(self) -> None:
        """Test the logout action when not logged in."""
        response = self.client.post(f"/{LOGOUT_ACTION_ROUTE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/{LOGIN_ROUTE}?error=User is not logged in.", 302, 200
        )
