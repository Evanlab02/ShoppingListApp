"""Contains the BaseTestCase class for API tests."""

import requests
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from authentication.tests.helpers import create_test_user
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


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
        self.store = Store.objects.create(
            name="Takealot",
            description="Online South African Store.",
            store_type=1,
            user=self.user,
        )
        self.store.save()

        self.item = Item.objects.create(
            name="Logitech G Pro X",
            description="Headphones for gamers.",
            price=2500,
            store=self.store,
            user=self.user,
        )
        self.item.save()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    def _login(self) -> None:
        """Test that a user can login."""
        url = f"{self.live_server_url}/api/v1/auth/login"
        data = {
            "username": self.mock_username,
            "password": self.mock_password,
        }
        self.session.post(url, json=data)
