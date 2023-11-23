"""Contains integration tests for the auth endpoints."""

from unittest import TestCase

import requests


class TestAuthEndpoints(TestCase):
    """Contains tests for the auth endpoints."""

    @classmethod
    def setUpClass(cls):
        """Create a requests session."""
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls):
        """Close the requests session."""
        cls.session.close()

    def test_1_register(self):
        """Test that a user can register."""
        url = "http://localhost:7001/api/auth/register"
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

    def test_2_login(self):
        """Test that a user can login."""
        url = "http://localhost:7001/api/auth/login"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")

    def test_3_login_again(self):
        """Test that a user can login again."""
        url = "http://localhost:7001/api/auth/login"
        data = {
            "username": "AuthTester1",
            "password": "AuthTester1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is already authenticated.")

    def test_4_register_again(self):
        """Test that a user cannot register again."""
        url = "http://localhost:7001/api/auth/register"
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
        self.assertEqual(response.json()["detail"], "User is already authenticated.")

    def test_5_get_token(self):
        """Test that a user can get their token."""
        url = "http://localhost:7001/api/auth/token"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        self.assertIn("message", response_json)

    def test_6_logout(self):
        """Test that a user can logout."""
        url = "http://localhost:7001/api/auth/logout"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged out.")

    def test_7_logout_again(self):
        """Test that a user cannot logout again."""
        url = "http://localhost:7001/api/auth/logout"
        response = self.session.get(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "User is not authenticated.")
