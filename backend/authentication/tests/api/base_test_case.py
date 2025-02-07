"""Contains the BaseTestCase class for API tests."""

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from authentication.tests.factory import ClientFactory, UserFactory


class BaseTestCase(StaticLiveServerTestCase):
    """Contains the base class for the API tests."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory()  # type: ignore
        self.client = Client()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test."""
        User.objects.all().delete()
        return super().tearDown()
