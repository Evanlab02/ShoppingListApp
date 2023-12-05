"""Contains tests for the authentication routes."""

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

REGISTER_ENDPOINT = "/api/v1/auth/register"
LOGIN_ENDPOINT = "/api/v1/auth/login"
CONTENT_TYPE = "application/json"
SUCCESS_REGISTER_MESSAGE = "User successfully registered."
SUCCESS_LOGIN_MESSAGE = "User successfully logged in."
TEST_EMAIL = "test@login.com"


class TestAuthentication(TestCase):
    """Tests for the authentication app."""

    def test_register(self) -> None:
        """Test the register endpoint."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test",
                "email": "test@testuser.com",
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"message": SUCCESS_REGISTER_MESSAGE, "detail": ""}
        )

    def test_register_with_already_logged_in_user(self) -> None:
        """Test the register endpoint with an already logged in user."""
        test_user = User.objects.create_user(
            username="testalreadyloggedin",
            email="testalreadyloggedin@gmail.com",
            password="testalreadyloggedinpassword",
        )
        test_user.save()

        client = Client()
        client.force_login(test_user)

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "testuser",
                "email": "testnewuser@user.com",
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "User is already logged in."})

    def test_register_with_incomplete_details(self) -> None:
        """Test the register endpoint with incomplete details."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test",
                "email": "",
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "",
                "last_name": "",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "detail": "Please ensure username, email, first name and last name are provided."
            },
        )

    def test_register_user_with_existing_username(self) -> None:
        """Test the register endpoint with an existing username."""
        test_user = User.objects.create_user(
            username="testuser",
            email="testusername@user.com",
            password="testuserpassword",
        )
        test_user.save()

        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "testuser",
                "email": "tester@test.com",
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Username already exists."})

    def test_register_user_with_existing_email(self) -> None:
        """Test the register endpoint with an existing email."""
        test_user = User.objects.create_user(
            username="testuser",
            email="testemail@user.com",
            password="testuserpassword",
        )
        test_user.save()

        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "tester",
                "email": "testemail@user.com",
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Email already exists."})

    def test_register_with_non_matching_passwords(self) -> None:
        """Test the register endpoint with non matching passwords."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test",
                "email": "testpassword@test.com",
                "password": "testpassword",
                "password_confirmation": "testpassword1",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {"detail": "Password and password confirmation do not match."},
        )

    def test_login_valid_credentials(self) -> None:
        """Test the login endpoint."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test-login",
                "email": TEST_EMAIL,
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"message": SUCCESS_REGISTER_MESSAGE, "detail": ""}
        )

        response = client.post(
            LOGIN_ENDPOINT,
            {"username": "test-login", "password": "testpassword"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": SUCCESS_LOGIN_MESSAGE, "detail": ""}
        )

    def test_login_retry(self) -> None:
        """Test the login endpoint."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test-login",
                "email": TEST_EMAIL,
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"message": SUCCESS_REGISTER_MESSAGE, "detail": ""}
        )

        response = client.post(
            LOGIN_ENDPOINT,
            {"username": "test-login", "password": "testpassword"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), {"message": SUCCESS_LOGIN_MESSAGE, "detail": ""}
        )

        response = client.post(
            LOGIN_ENDPOINT,
            {"username": "test-login", "password": "testpassword"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "User is already logged in."})

    def test_login_invalid_credentials(self) -> None:
        """Test the login endpoint."""
        client = Client()

        response = client.post(
            REGISTER_ENDPOINT,
            {
                "username": "test-login",
                "email": TEST_EMAIL,
                "password": "testpassword",
                "password_confirmation": "testpassword",
                "first_name": "test",
                "last_name": "user",
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(), {"message": SUCCESS_REGISTER_MESSAGE, "detail": ""}
        )

        response = client.post(
            LOGIN_ENDPOINT,
            {"username": "test-login", "password": "test"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid Credentials."})
