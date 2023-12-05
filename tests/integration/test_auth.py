"""Contains integration tests for the auth endpoints."""

from unittest import TestCase

import requests


class TestAuthEndpoints(TestCase):
    """Contains tests for the auth endpoints."""

    session: requests.Session

    @classmethod
    def setUpClass(cls) -> None:
        """Create a requests session."""
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the requests session."""
        cls.session.close()

    def test_1_register(self) -> None:
        """Test that a user can register."""
        url = "http://localhost:7001/api/v1/auth/register"
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

    def test_2_login(self) -> None:
        """Test that a user can login."""
        url = "http://localhost:7001/api/v1/auth/login"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")
        self.assertEqual(response.json()["detail"], "")

    def test_3_login_again(self) -> None:
        """Test that a user cannot login again."""
        url = "http://localhost:7001/api/v1/auth/login"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already logged in.")

    def test_4_register_again(self) -> None:
        """Test that a user cannot register again."""
        url = "http://localhost:7001/api/v1/auth/register"
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

    def test_5_get_token(self) -> None:
        """Test that a user can get their token."""
        url = "http://localhost:7001/api/v1/auth/token"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertEqual(response_json["message"], "Token successfully retrieved.")
        self.assertIn("detail", response_json)

    def test_6_logout(self) -> None:
        """Test that a user can logout."""
        url = "http://localhost:7001/api/v1/auth/logout"
        response = self.session.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged out.")

    def test_7_logout_again(self) -> None:
        """Test that a user cannot logout again."""
        url = "http://localhost:7001/api/v1/auth/logout"
        response = self.session.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is not logged in.")
