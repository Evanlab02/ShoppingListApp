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

        self.other_user = UserFactory.create()

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

    async def test_get_item_for_user(self) -> None:
        """Test the get item for user method."""
        item = await self.item_service.get_item_for_user(item_id=self.item.id, user=self.user)
        self.assertEqual(item.id, self.item.id)
        self.assertEqual(item.name, self.item.name)
        self.assertEqual(item.price, self.item.price)

    async def test_get_item_for_user_that_does_not_exist(self) -> None:
        """Test the get item for user method when the item does not exist."""
        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.get_item_for_user(item_id=99999, user=self.user)

        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.get_item_for_user(item_id=self.item.id, user=self.other_user)
