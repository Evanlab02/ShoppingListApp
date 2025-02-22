"""Contains tests for the get_item function of the item repository."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory

MOCK_NAME = "Test Item"
MOCK_DESCRIPTION = "Test Description"


class TestItemRepositoryDetail(TestCase):
    """Test the item repository get_item function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        self.item = ItemFactory.create(user=self.user, store=self.store)
        self.create_item = sync_to_async(ItemFactory.create)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Store.objects.all().delete()
        Item.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_get_item(self) -> None:
        """Test getting a single item by ID."""
        retrieved_item = await self.repo.get_item(self.item.id)

        self.assertEqual(retrieved_item.id, self.item.id)
        self.assertEqual(retrieved_item.name, self.item.name)
        self.assertEqual(retrieved_item.description, self.item.description)
        self.assertEqual(retrieved_item.price, self.item.price)
        self.assertEqual(retrieved_item.user.id, self.user.id)
        self.assertEqual(retrieved_item.store.id, self.store.id)

    async def test_get_item_for_user(self) -> None:
        """Test getting a single item by ID for a specific user."""
        retrieved_item = await self.repo.get_item_for_user(self.item.id, self.user)

        self.assertEqual(retrieved_item.id, self.item.id)
        self.assertEqual(retrieved_item.name, self.item.name)
        self.assertEqual(retrieved_item.description, self.item.description)
        self.assertEqual(retrieved_item.price, self.item.price)
        self.assertEqual(retrieved_item.user.id, self.user.id)
        self.assertEqual(retrieved_item.store.id, self.store.id)

    async def test_get_item_for_user_not_found(self) -> None:
        """Test getting a non-existent item for a specific user raises DoesNotExist."""
        item = await self.create_item(store=self.store)
        with self.assertRaises(Item.DoesNotExist):
            await self.repo.get_item_for_user(item.id, self.user)
