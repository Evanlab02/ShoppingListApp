"""Tests the logout action."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLogoutAction(TestCase):
    """
    Test the logout action route.

    Tests: authentication.views.logout_action
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        1. Setup the test client.
        2. Create a test user.
        3. Call the super setup method.
        """
        self.client = Client()
        self.user = UserFactory.create()
        return super().setUp()

    def tearDown(self) -> None:
        """
        Tear down the test environment.

        1. Logout the test user.
        2. Call the super teardown method.
        """
        self.client.logout()
        return super().tearDown()

    def test_logout_action(self) -> None:
        """
        Test the logout action.

        Given: The user is logged in.
        When: The user logs out via this view.
        Then: The user is redirected to the login page.
        """
        self.client.force_login(self.user)
        response = self.client.post(reverse("logout_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login_page"), 302, 200)

    def test_get_logout_action_405(self) -> None:
        """
        Test the logout action returns 405 if a get request is made.

        Given: The user is logged in.
        When: The user visits the logout action endpoint using a get request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.get(reverse("logout_action"))
        self.assertEqual(response.status_code, 405)

    def test_logout_action_when_not_logged_in(self) -> None:
        """
        Test the logout action when not logged in.

        Given: The user is not logged in.
        When: The user logs out via this view.
        Then: The user is redirected to the login page with an error message.
        """
        response = self.client.post(reverse("logout_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login_page')}?error=You must be logged in to access that page.",
            302,
            200,
        )
