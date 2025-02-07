"""Contains tests for the authentication routes."""

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from authentication.tests.factory import NewUserSchemaFactory, UserFactory

CONTENT_TYPE = "application/json"
SUCCESS_REGISTER_MESSAGE = "User successfully registered."
SUCCESS_LOGIN_MESSAGE = "User successfully logged in."
TEST_EMAIL = "test@login.com"


class TestAuthentication(TestCase):
    """Tests for the authentication app."""

    def setUp(self) -> None:
        """Set up the test."""
        self.client = Client()

    def test_register(self) -> None:
        """Test the register endpoint."""
        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory().model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message": SUCCESS_REGISTER_MESSAGE, "detail": ""})

    def test_register_with_already_logged_in_user(self) -> None:
        """Test the register endpoint with an already logged in user."""
        test_user = UserFactory()
        self.client.force_login(test_user)

        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory().model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "User is already logged in."})

    def test_register_with_incomplete_details(self) -> None:
        """Test the register endpoint with incomplete details."""
        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory(
                username="",
                email="",
                password="",
                password_confirmation="",
                first_name="",
                last_name="",
            ).model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Please ensure username, email, first name and last name are provided."},
        )

    def test_register_user_with_existing_username(self) -> None:
        """Test the register endpoint with an existing username."""
        UserFactory(username="testuser")

        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory(
                username="testuser",
                email="testusername@user.com",
                password="testuserpassword",
                password_confirmation="testuserpassword",
                first_name="test",
                last_name="user",
            ).model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Username already exists."})

    def test_register_user_with_existing_email(self) -> None:
        """Test the register endpoint with an existing email."""
        UserFactory(email="testemail@user.com")

        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory(
                username="testuser",
                email="testemail@user.com",
                password="testpassword",
                password_confirmation="testpassword",
                first_name="test",
                last_name="user",
            ).model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Email already exists."})

    def test_register_with_non_matching_passwords(self) -> None:
        """Test the register endpoint with non matching passwords."""
        response = self.client.post(
            reverse("ninja-api:auth_register"),
            NewUserSchemaFactory(
                username="test",
                email="testpassword@test.com",
                password="testpassword",
                password_confirmation="testpassword1",
                first_name="test",
                last_name="user",
            ).model_dump(),
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Password and password confirmation do not match."},
        )

    def test_login_valid_credentials(self) -> None:
        """Test the login endpoint."""
        user = UserFactory()

        response = self.client.post(
            reverse("ninja-api:auth_login"),
            {"username": user.username, "password": "test"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": SUCCESS_LOGIN_MESSAGE, "detail": ""})

    def test_login_while_already_logged_in(self) -> None:
        """Test the login endpoint while already logged in."""
        user = UserFactory()

        self.client.force_login(user)

        response = self.client.post(
            reverse("ninja-api:auth_login"),
            {"username": user.username, "password": "test"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "User is already logged in."})

    def test_login_invalid_credentials(self) -> None:
        """Test the login endpoint."""
        response = self.client.post(
            reverse("ninja-api:auth_login"),
            {"username": "invaliduser", "password": "invalidpassword"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid Credentials."})

    def test_logout(self) -> None:
        """Test the logout endpoint."""
        user = UserFactory()

        self.client.force_login(user)

        response = self.client.post(reverse("ninja-api:auth_logout"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": "User successfully logged out.", "detail": ""}
        )

    def test_logout_without_being_logged_in(self) -> None:
        """Test the logout endpoint."""
        response = self.client.post(reverse("ninja-api:auth_logout"))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "User is not logged in."})
