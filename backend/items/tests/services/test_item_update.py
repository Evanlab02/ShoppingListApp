"""Tests for the item update service."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.errors.exceptions import StoreDoesNotExist
from stores.tests.factory import StoreFactory


class ItemUpdateServiceTestCase(TestCase):
    """Tests for the item update service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(store=self.store, user=self.user)
        self.new_store = StoreFactory.create(user=self.user)
        self.matching_item = ItemFactory.create(
            store=self.new_store,
            user=self.user,
            name="Matching Item",
        )
        self.create = sync_to_async(ItemFactory.create)

    async def test_update_item(self) -> None:
        """Test the update item method."""
        updated_item = await self.item_service.update_item(
            item_id=self.item.id,
            user=self.user,
            new_store_id=self.new_store.id,
            new_name="New Name",
            new_price=100.00,
            new_description="New Description",
        )
        new_store = await updated_item.astore()
        self.assertEqual(updated_item.name, "New Name")
        self.assertEqual(updated_item.price, 100.00)
        self.assertEqual(updated_item.description, "New Description")
        self.assertEqual(new_store.id, self.new_store.id)

    async def test_update_with_invalid_item_id(self) -> None:
        """Test the update item method with an invalid item id."""
        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.update_item(
                item_id=99999,
                user=self.user,
            )

    async def test_update_item_to_match_existing_item(self) -> None:
        """Test the update item method when the item already exists."""
        self.item.name = self.matching_item.name
        await self.item.asave()

        with self.assertRaises(ItemAlreadyExists):
            await self.item_service.update_item(
                item_id=self.item.id,
                user=self.user,
                new_store_id=self.new_store.id,
                new_name=self.matching_item.name,
            )

    async def test_update_item_name(self) -> None:
        """Test the update item method when the name is updated."""
        await self.item_service.update_item(
            item_id=self.item.id,
            user=self.user,
            new_name="New Name",
        )
        await self.item.arefresh_from_db()
        self.assertEqual(self.item.name, "New Name")

    async def test_update_item_that_does_not_exist(self) -> None:
        """Test the update item method when the item does not exist."""
        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.update_item(
                item_id=99999,
                user=self.user,
            )

    async def test_update_item_store(self) -> None:
        """Test the update item method when the store is updated."""
        new_store = await self.create(user=self.user)
        await self.item_service.update_item(
            item_id=self.item.id,
            user=self.user,
            new_store_id=new_store.id,
        )
        await self.item.arefresh_from_db()
        store = await self.item.astore()
        self.assertEqual(store.id, new_store.id)

    async def test_update_prevents_duplicates(self) -> None:
        """Test the update item method when the name is updated to a duplicate item."""
        await self.create(name="Duplicate Item", store=self.store, user=self.user)
        with self.assertRaises(ItemAlreadyExists):
            await self.item_service.update_item(
                item_id=self.item.id,
                user=self.user,
                new_name="Duplicate Item",
            )

    async def test_update_item_store_to_one_that_does_not_exist(self) -> None:
        """Test the update item method when the store does not exist."""
        with self.assertRaises(StoreDoesNotExist):
            await self.item_service.update_item(
                item_id=self.item.id,
                user=self.user,
                new_store_id=99999,
            )
