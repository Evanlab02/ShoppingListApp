"""Test the delete functionality in the item service."""

from items.errors.exceptions import ItemDoesNotExist
from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase
from items.services import item_service
from shoppingapp.schemas.shared import DeleteSchema


class TestItemServiceDelete(BaseTestCase):
    """Test the item service delete functionality."""

    async def test_delete_item_output(self) -> None:
        """Test the delete function output."""
        result = await item_service.delete_item(self.item.id, self.user)
        self.assertIsInstance(result, DeleteSchema)

        result_dict = result.model_dump()
        self.assertEqual(result_dict["message"], "Deleted Item.")
        self.assertEqual(result_dict["detail"], f"Item with ID #{self.item.id} was deleted.")

    async def test_delete_item(self) -> None:
        """Test the delete item function."""
        await item_service.delete_item(self.item.id, self.user)

        # Check if the item was deleted.
        item_exists = await Item.objects.filter(id=self.item.id).aexists()
        self.assertFalse(item_exists)

    async def test_delete_item_invalid_id(self) -> None:
        """Test deleting an item with an invalid id."""
        with self.assertRaises(ItemDoesNotExist):
            await item_service.delete_item(999999, self.user)

    async def test_delete_item_invalid_user(self) -> None:
        """Test deleting an item with an invalid user."""
        user = await self.create_temporary_user()
        with self.assertRaises(ItemDoesNotExist):
            await item_service.delete_item(self.item.id, user)
