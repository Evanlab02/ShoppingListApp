"""Contains tests for the create function of the item repository."""

from datetime import datetime

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory

MOCK_NAME = "Test Item"
MOCK_DESRIPTION = "Test Description"


class TestItemRepositoryCreate(TestCase):
    """Test the item repository create function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    async def test_create_item(self) -> None:
        """Test the create item function."""
        item = await self.repo.create_item(
            user=self.user,
            store=self.store,
            price=100,
            name=MOCK_NAME,
            description=MOCK_DESRIPTION,
        )

        self.assertEqual(item.name, MOCK_NAME)
        self.assertEqual(item.description, MOCK_DESRIPTION)
        self.assertEqual(item.price, 100)
        self.assertEqual(item.user, self.user)
        self.assertEqual(item.store, self.store)
        self.assertIsInstance(item.created_at, datetime)
        self.assertIsInstance(item.updated_at, datetime)

        exists = await Item.objects.filter(user=self.user, name=MOCK_NAME).aexists()
        self.assertTrue(exists)
