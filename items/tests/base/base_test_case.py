"""Contains the base test case for the item application."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


class BaseTestCase(TestCase):
    """Base test case for the item application."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        self.store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        self.item = Item.objects.create(
            name="Test Item",
            description="Test Description",
            price=100,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        self.alt_item = Item.objects.create(
            name="Alternate Item",
            description="Alternate Description",
            price=200,
            store=self.store,
            user=self.user,
        )
        self.alt_item.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Item.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()
