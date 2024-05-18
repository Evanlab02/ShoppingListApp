"""Contains tests for the item repository delete functions."""

from items.database import item_repo
from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestDeleteItem(BaseTestCase):
    """Test the item repo delete functions."""

    async def test_delete_item(self) -> None:
        """Test deleting an item."""
        # Delete the item
        await item_repo.delete_item(item_id=self.item.id, user=self.user)

        # Check that the item no longer exists
        item_exists = await Item.objects.filter(id=self.item.id).aexists()
        self.assertFalse(item_exists)

    async def test_delete_item_invalid_id(self) -> None:
        """Test deleting an item with an invalid id."""
        with self.assertRaises(Item.DoesNotExist):
            await item_repo.delete_item(item_id=100, user=self.user)

        # Check that the item still exists
        item_exists = await Item.objects.filter(id=self.item.id).aexists()
        self.assertTrue(item_exists)

    async def test_delete_item_invalid_user(self) -> None:
        """Test deleting an item with an invalid user."""
        user = await self.create_temporary_user()
        with self.assertRaises(Item.DoesNotExist):
            await item_repo.delete_item(item_id=self.item.id, user=user)

        # Check that the item still exists
        item_exists = await Item.objects.filter(id=self.item.id).aexists()
        self.assertTrue(item_exists)
