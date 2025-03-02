"""Tests for the get item list service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemListServiceTestCase(TestCase):
    """Tests for the get item list service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.items = ItemFactory.create_batch(size=10, store=self.store, user=self.user)

    async def test_get_item_list(self) -> None:
        """Test the get item list method."""
        items = await self.item_service.get_items(user=self.user)
        self.assertEqual(len(items.items), 10)
        self.assertEqual(items.total, 10)
        self.assertEqual(items.total_pages, 1)

        for item in items.items:
            self.assertIn(item.model_dump().get("id"), [item.id for item in self.items])

    async def test_search_items(self) -> None:
        """Test the search items method."""
        items = await self.item_service.search_items(user=self.user)
        self.assertEqual(len(items.items), 10)
        self.assertEqual(items.total, 10)
        self.assertEqual(items.total_pages, 1)

        for item in items.items:
            self.assertIn(item.model_dump().get("id"), [item.id for item in self.items])
