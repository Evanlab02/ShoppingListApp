"""Contains tests for the does_item_exist function of the item repository."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestDoesItemExist(TestCase):
    """Test the does_item_exist function of the item repository."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.repo = ItemRepo()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(user=self.user, store=self.store)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_does_item_exist(self) -> None:
        """Test the does_item_exist function of the item repository."""
        self.assertTrue(await self.repo.does_item_exist(self.item.name, None))

    async def test_does_item_exist_with_store(self) -> None:
        """Test the does_item_exist function of the item repository with a store."""
        self.assertTrue(await self.repo.does_item_exist(self.item.name, self.store.id))

    async def test_item_does_not_exist(self) -> None:
        """Test the does_item_exist function of the item repository with a non-existent item."""
        self.assertFalse(await self.repo.does_item_exist("Non-existent item", None))

    async def test_item_does_not_exist_with_store(self) -> None:
        """Test does_item_exist with a non-existent item and store."""
        self.assertFalse(await self.repo.does_item_exist("Non-existent item", self.store.id))
