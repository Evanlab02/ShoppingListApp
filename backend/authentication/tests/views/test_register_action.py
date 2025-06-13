"""Contains tests for the register action view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory

TEST_EMAIL = "user@test.com"


class TestRegisterActionView(TestCase):
    """
    Test the register action view.

    Tests: authentication.views.register_action
    """

    def setUp(self) -> None:
        """Set up the test environment.

        1. Setup the test client.
        2. Create a test user.
        3. Call the super setup method.
        """
        self.client = Client()
        self.user = UserFactory.create()
        super().setUp()

    def test_register_action_endpoint(self) -> None:
        """
        Test the register action endpoint.

        Given: The user is not logged in.
        When: The user registers via this view.
        Then: The user is redirected to the login page.
        """
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "registeruser",
                "password": "testpassword",
                "email": TEST_EMAIL,
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("login_page"),
            302,
            200,
        )

    def test_get_register_action_endpoint_405(self) -> None:
        """
        Test the register action endpoint returns 405 if a get request is made.

        Given: The user is not logged in.
        When: The user visits the register action endpoint using a get request.
        Then: The user receives a 405 status code as this method is not allowed.
        """
        response = self.client.get(reverse("register_action"))
        self.assertEqual(response.status_code, 405)

    def test_register_action_endpoint_when_already_logged_in(self) -> None:
        """
        Test the register action endpoint redirects when the user is already logged in.

        Given: The user is logged in.
        When: The user attempts to register via this view.
        Then: The user is redirected to the dashboard as they are already logged in.
        """
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "registeruser",
                "password": "testpassword",
                "email": TEST_EMAIL,
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("dashboard"),
            302,
            200,
        )

    def test_register_action_endpoint_with_invalid_username(self) -> None:
        """
        Test the register action endpoint with an invalid username.

        Given: The user is not logged in.
        When: The user attempts to register via this view with an invalid username.
        Then: The user is redirected back to the register page with an error message.
        """
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "",
                "password": "testpassword",
                "email": TEST_EMAIL,
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("register_page")
            + "?error=Please ensure username, email, first name and last name are provided.",  # noqa: E501
            302,
            200,
        )

    def test_register_action_endpoint_with_invalid_password(self) -> None:
        """
        Test the register action endpoint with an invalid password.

        Given: The user is not logged in.
        When: The user attempts to register via this view with an invalid password.
        Then: The user is redirected back to the register page with an error message.
        """
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "registeruser",
                "password": "abcd",
                "email": TEST_EMAIL,
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("register_page") + "?error=Password and password confirmation do not match.",
            302,
            200,
        )

    def test_register_action_endpoint_already_existing_username(self) -> None:
        """
        Test the register action endpoint with an already existing username.

        Given: The user is not logged in.
        When: The user attempts to register via this view with an already existing username.
        Then: The user is redirected back to the register page with an error message.
        """
        UserFactory.create(username="testuser")
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "testuser",
                "password": "testpassword",
                "email": TEST_EMAIL,
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("register_page") + "?error=Username already exists.",
            302,
            200,
        )

    def test_register_action_endpoint_already_existing_email(self) -> None:
        """
        Test the register action endpoint with an already existing email.

        Given: The user is not logged in.
        When: The user attempts to register via this view with an already existing email.
        Then: The user is redirected back to the register page with an error message.
        """
        UserFactory.create(username="random_very_random_username", email="duplicate@gmail.com")
        response = self.client.post(
            reverse("register_action"),
            {
                "username": "registeruser",
                "password": "testpassword",
                "email": "duplicate@gmail.com",
                "first_name": "test",
                "last_name": "user",
                "password_confirm": "testpassword",
            },
        )
        self.assertRedirects(
            response,
            reverse("register_page") + "?error=Email already exists.",
            302,
            200,
        )
