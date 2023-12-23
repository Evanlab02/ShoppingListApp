"""Contains integration tests for the stores endpoints."""

from unittest import TestCase

import requests

from authentication.constants import INPUT_MAPPING

CREATE_URL = "http://localhost:7001/api/v1/stores/create"
MAPPING_URL = "http://localhost:7001/api/v1/stores/types/mapping"
LOGIN_URL = "http://localhost:7001/"
TOKEN_URL = "http://localhost:7001/token/register"
DASHBOARD_URL = "http://localhost:7001/shopping/dashboard/"
USERNAME_INPUT = INPUT_MAPPING.get("username-input", "username-input")
PASSWORD_INPUT = INPUT_MAPPING.get("password-input", "password-input")
SUBMIT_LOGIN = INPUT_MAPPING.get("submit-login", "submit-login")
TOKEN_ID = "api-token"


class TestStoreEndpoints(TestCase):
    """Contains tests for the store endpoints."""

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
            "username": "StoreUser1",
            "password": "StoreUser1",
            "password_confirmation": "StoreUser1",
            "email": "StoreUser1@gmail.com",
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
            "username": "StoreUser1",
            "password": "StoreUser1",
        }
        response = self.session.post(url, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "User successfully logged in.")
        self.assertEqual(response.json()["detail"], "")

    def test_3_create_store(self) -> None:
        """Test that a user can create a store."""
        payload = {
            "name": "StoreTester1",
            "description": "StoreTester1",
            "store_type": 3,
        }
        response = self.session.post(CREATE_URL, json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "StoreTester1")
        self.assertEqual(response.json()["description"], "StoreTester1")
        self.assertEqual(response.json()["store_type"], 3)
        self.assertIsInstance(response.json()["id"], int)
        self.assertIsInstance(response.json()["created_at"], str)
        self.assertIsInstance(response.json()["updated_at"], str)

    def test_4_get_store_type_mapping(self) -> None:
        """Test that a user can get the store type mapping."""
        response = self.session.get(MAPPING_URL)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)
        self.assertEqual(response.json()["1"], "Online")
        self.assertEqual(response.json()["2"], "In-Store")
        self.assertEqual(response.json()["3"], "Both")
