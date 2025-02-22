"""Tests for the item create service."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.errors.exceptions import ItemAlreadyExists
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemCreateServiceTestCase(TestCase):
    """Tests for the item create service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.create = sync_to_async(ItemFactory.create)

    async def test_create_item(self) -> None:
        """Test the create item method."""
        item = await self.item_service.create_item(
            user=self.user,
            store_id=self.store.id,
            name="Test Item",
            price=10.0,
        )
        store = await item.astore()
        user = await item.auser()
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 10.0)
        self.assertEqual(store.id, self.store.id)
        self.assertEqual(user.id, self.user.id)

    async def test_create_item_with_duplicate_name(self) -> None:
        """Test the create item method with a duplicate name."""
        await self.create(name="Test Item", store=self.store, user=self.user)
        with self.assertRaises(ItemAlreadyExists):
            await self.item_service.create_item(
                user=self.user,
                store_id=self.store.id,
                name="Test Item",
                price=10.0,
            )
