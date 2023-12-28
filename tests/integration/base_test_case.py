"""Contains the BaseTestCase class for integration tests."""

from unittest import TestCase

import requests


class BaseTestCase(TestCase):
    """Contains the BaseTestCase class for integration tests."""

    session: requests.Session
    mock_username: str = "basetestuser1"
    mock_password: str = "testuser"

    @classmethod
    def setUpClass(cls) -> None:
        """Create a requests session."""
        cls.session = requests.Session()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the requests session."""
        cls.session.close()

    def _login(self) -> None:
        """Test that a user can login."""
        url = "http://localhost:7001/api/v1/auth/login"
        data = {
            "username": self.mock_username,
            "password": self.mock_password,
        }
        self.session.post(url, json=data)
