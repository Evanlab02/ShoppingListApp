"""Contains the BaseTestCase class for API tests."""

import requests
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from authentication.tests.helpers import create_test_user


class BaseTestCase(StaticLiveServerTestCase):
    """Contains the base class for the API tests."""

    session: requests.Session
    mock_username: str = "test"
    mock_password: str = "test"

    @classmethod
    def setUpClass(cls) -> None:
        """Create a requests session."""
        cls.session = requests.Session()
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        """Close the requests session."""
        cls.session.close()
        super().tearDownClass()

    def setUp(self) -> None:
        """Set up the test."""
        self.user = create_test_user()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test."""
        User.objects.all().delete()
        return super().tearDown()

    def _login(self) -> None:
        """Test that a user can login."""
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": self.mock_username,
            "password": self.mock_password,
        }
        self.session.post(url, json=data)
