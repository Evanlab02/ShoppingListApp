"""Tests for the item detail service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.errors.exceptions import ItemDoesNotExist
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemDetailServiceTestCase(TestCase):
    """Tests for the item detail service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(store=self.store, user=self.user)

    async def test_get_item_detail(self) -> None:
        """Test the get item detail method."""
        item = await self.item_service.get_item_detail(item_id=self.item.id)
        store = await self.item.astore()
        user = await self.item.auser()

        self.assertEqual(item.id, self.item.id)
        self.assertEqual(item.name, self.item.name)
        self.assertEqual(item.price, self.item.price)
        self.assertEqual(store.id, self.store.id)
        self.assertEqual(user.id, self.user.id)

    async def test_get_item_detail_that_does_not_exist(self) -> None:
        """Test the get item detail method when the item does not exist."""
        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.get_item_detail(item_id=99999)
