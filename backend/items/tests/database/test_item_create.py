"""Contains tests for the create function of the item repository."""

from datetime import datetime

from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
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

    async def test_create_item(self) -> None:
        """Test the create item function."""
        item = await self.repo.create_item(
            user=self.user,
            store_id=self.store.id,
            price=100,
            name=MOCK_NAME,
            description=MOCK_DESRIPTION,
        )

        await item.arefresh_from_db()
        self.assertEqual(item.name, MOCK_NAME)
        self.assertEqual(item.description, MOCK_DESRIPTION)
        self.assertEqual(item.price, 100)
        self.assertEqual(await item.auser(), self.user)
        self.assertEqual(await item.astore(), self.store)
        self.assertIsInstance(item.created_at, datetime)
        self.assertIsInstance(item.updated_at, datetime)

        exists = await Item.objects.filter(user=self.user, name=MOCK_NAME).aexists()
        self.assertTrue(exists)
