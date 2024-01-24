"""Contains the tests for the populate command."""

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from stores.models import ShoppingStore as Store


class PopulateTestCase(TestCase):
    """Test the populate command."""

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        return super().tearDown()

    def test_populate_command(self) -> None:
        """Test the populate command."""
        call_command("populate", *[], **{})

        # Check that the user was created
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.get(username="basetestuser1")
        self.assertEqual(user.email, "testuser@gmail.com")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")

        # Check that the store was created
        self.assertEqual(Store.objects.count(), 1)
        store = Store.objects.get(name="Base Test Store")
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, "This is a test store.")
        self.assertEqual(store.user, user)
