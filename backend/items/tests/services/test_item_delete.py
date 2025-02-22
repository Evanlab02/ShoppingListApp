"""Contains tests for the item delete service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.errors.exceptions import ItemDoesNotExist
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemDeleteServiceTestCase(TestCase):
    """Tests for the item delete service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(store=self.store, user=self.user)

    async def test_delete_item(self) -> None:
        """Test the delete item method."""
        result = await self.item_service.delete_item(item_id=self.item.id, user=self.user)
        self.assertEqual(result.message, "Deleted Item.")
        self.assertEqual(result.detail, f"Item with ID #{self.item.id} was deleted.")

    async def test_delete_item_that_does_not_exist(self) -> None:
        """Test the delete item method when the item does not exist."""
        with self.assertRaises(ItemDoesNotExist):
            await self.item_service.delete_item(item_id=99999, user=self.user)
