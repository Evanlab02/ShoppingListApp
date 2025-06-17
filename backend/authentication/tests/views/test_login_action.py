"""Contains tests for the login action view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory


class TestLoginAction(TestCase):
    """
    Test the login action view.

    Tests: authentication.views.login_action
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        1. Setup the test client.
        2. Create a test user.
        3. Call the super setup method.
        """
        self.client = Client()
        self.user = UserFactory.create(username="testuser")
        super().setUp()

    def tearDown(self) -> None:
        """
        Tear down the test environment.

        1. Logout the test user.
        2. Call the super teardown method.
        """
        self.client.logout()
        return super().tearDown()

    def test_login_action_endpoint(self) -> None:
        """
        Test the login action view redirects when the user logs in.

        Given: The user is not logged in.
        When: The user logs in via this view.
        Then: The user is redirected to the dashboard.
        """
        response = self.client.post(
            reverse("login_action"),
            {
                "username": "testuser",
                "password": "test",
            },
        )
        self.assertRedirects(
            response,
            reverse("dashboard"),
            302,
            200,
        )

    def test_get_login_action_endpoint_405(self) -> None:
        """
        Test the login action view returns 405 if a get request is made.

        Given: The user is not logged in.
        When: The user visits the login action endpoint using a get request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.get(reverse("login_action"))
        self.assertEqual(response.status_code, 405)

    def test_login_action_endpoint_when_logged_in(self) -> None:
        """
        Test the login action endpoint redirects if the user is already logged in.

        Given: The user is logged in.
        When: The user logs attempts to log in via this view.
        Then: The user is redirected to the dashboard.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("login_action"),
            {
                "username": "testuser",
                "password": "test",
            },
        )
        self.assertRedirects(
            response,
            reverse("dashboard"),
            302,
            200,
        )

    def test_login_action_endpoint_with_invalid_credentials(self) -> None:
        """
        Test the login action view with invalid credentials.

        Redirects to login page with error message if the user attempts to log in with invalid
        credentials.

        Given: The user is not logged in.
        When: The user attempts to log in via this view with invalid credentials.
        Then: The user is redirected to the login page with an error message.
        """
        response = self.client.post(
            reverse("login_action"),
            {
                "username": "testuser",
                "password": "invalidpassword",
            },
        )
        self.assertRedirects(
            response,
            f"{reverse('login_page')}?error=Invalid Credentials.",
            302,
            200,
        )
