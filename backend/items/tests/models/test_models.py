"""Test item app models."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestItemsApp(TestCase):
    """Test the items app."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(user=self.user, store=self.store)
        return super().setUp()

    def test_item_model_to_string(self) -> None:
        """Test the item model to string method."""
        self.assertEqual(str(self.item), f"{self.item.name}@{self.item.store.name}")

    async def test_get_store(self) -> None:
        """Test the get store method."""
        store = await self.item.astore()
        self.assertEqual(store, self.store)

    async def test_get_user(self) -> None:
        """Test the get user method."""
        user = await self.item.auser()
        self.assertEqual(user, self.user)
