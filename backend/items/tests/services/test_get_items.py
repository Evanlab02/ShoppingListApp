"""Contains tests for the get items service."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestGetItemsService(TestCase):
    """Tests for the get items service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(store=self.store, user=self.user)

        self.bulk_create = sync_to_async(ItemFactory.create_batch)

    async def test_get_items(self) -> None:
        """Test the get items method."""
        items = await self.item_service.get_items(user=self.user)
        self.assertEqual(len(items.items), 1)

        item = items.items[0]
        item_dict = item.model_dump()
        self.assertEqual(item_dict.get("id"), self.item.id)
        self.assertEqual(item_dict.get("name"), self.item.name)
        self.assertEqual(item_dict.get("price"), self.item.price)
        self.assertEqual(item_dict.get("description"), self.item.description)
        self.assertIsNotNone(item_dict.get("created_at"))
        self.assertIsNotNone(item_dict.get("updated_at"))

        self.assertEqual(item_dict.get("store", {}).get("id"), self.store.id)
        self.assertEqual(item_dict.get("store", {}).get("name"), self.store.name)
        self.assertEqual(item_dict.get("store", {}).get("store_type"), self.store.store_type)
        self.assertEqual(item_dict.get("store", {}).get("description"), self.store.description)
        self.assertIsNotNone(item_dict.get("store", {}).get("created_at"))
        self.assertIsNotNone(item_dict.get("store", {}).get("updated_at"))

        self.assertEqual(item_dict.get("user", {}).get("username"), self.user.username)

        self.assertEqual(items.total, 1)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertFalse(items.has_previous)
        self.assertFalse(items.has_next)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_get_items_with_100_items(self) -> None:
        """Test the get items method with 100 items."""
        await self.bulk_create(99, store=self.store, user=self.user)
        items = await self.item_service.get_items(user=self.user, page=1, items_per_page=5)

        self.assertEqual(len(items.items), 5)
        self.assertEqual(items.total, 100)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 20)
        self.assertTrue(items.has_next)
        self.assertEqual(items.next_page, 2)
        self.assertFalse(items.has_previous)
        self.assertIsNone(items.previous_page)

        items = await self.item_service.get_items(user=self.user, page=2, items_per_page=5)
        self.assertEqual(len(items.items), 5)
        self.assertEqual(items.total, 100)
        self.assertEqual(items.page_number, 2)
        self.assertEqual(items.total_pages, 20)
        self.assertTrue(items.has_previous)
        self.assertEqual(items.previous_page, 1)
        self.assertTrue(items.has_next)
        self.assertEqual(items.next_page, 3)

        items = await self.item_service.get_items(user=self.user, page=20, items_per_page=5)
        self.assertEqual(len(items.items), 5)
        self.assertEqual(items.total, 100)
        self.assertEqual(items.page_number, 20)
        self.assertEqual(items.total_pages, 20)
        self.assertTrue(items.has_previous)
        self.assertEqual(items.previous_page, 19)
        self.assertFalse(items.has_next)
        self.assertIsNone(items.next_page)
