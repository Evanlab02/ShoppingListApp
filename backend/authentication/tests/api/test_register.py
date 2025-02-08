"""Contains the register API tests."""

from authentication.tests.api.base_test_case import BaseTestCase
from authentication.tests.factory import NewUserSchemaFactory


class RegisterAPITests(BaseTestCase):
    """Register api tests."""

    def test_register(self) -> None:
        """Test that a user can register."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create().model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["message"], "User successfully registered.")
        self.assertEqual(response.json()["detail"], "")

    def test_register_when_logged_in(self) -> None:
        """Test that a user cannot register when logged in."""
        self.client.force_login(self.user)
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create().model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already logged in.")

    def test_register_with_invalid_email(self) -> None:
        """Test that a user cannot register with invalid credentials."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create(email="").model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"],
            "Please ensure username, email, first name and last name are provided.",
        )

    def test_register_with_username_that_already_exists(self) -> None:
        """Test that a user cannot register with a username that already exists."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create(username=self.user.username).model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Username already exists.")

    def test_register_with_email_that_already_exists(self) -> None:
        """Test that a user cannot register with an email that already exists."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create(email=self.user.email).model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Email already exists.")

    def test_register_with_password_and_password_confirmation_that_do_not_match(self) -> None:
        """Test that a user cannot register when passwords do not match."""
        url = f"{self.live_server_url}/api/v1/auth/register"
        data = NewUserSchemaFactory.create(
            password="password", password_confirmation="password2"
        ).model_dump()
        response = self.client.post(url, data=data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], "Password and password confirmation do not match."
        )
