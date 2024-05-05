"""Contains tests for the item service update function."""

from items.errors.exceptions import ItemDoesNotExist
from items.models import ShoppingItem as Item
from items.services import item_service
from items.tests.base.base_test_case import BaseTestCase


class TestUpdateItemService(BaseTestCase):
    """Test the item service update function."""

    async def test_update_item_with_no_changes(self) -> None:
        """Test updating an item with no changes."""
        item_before_update = await Item.objects.aget(id=self.item.id)
        item = await item_service.update_item(item_id=self.item.id)
        item_dict = item.model_dump()

        self.assertEqual(item_before_update.id, item_dict.get("id"))  # ID remains the same
        self.assertEqual(item_before_update.name, item_dict.get("name"))  # Name remains the same
        self.assertEqual(item_before_update.price, item_dict.get("price"))  # Price remains the same

        # Updated at changes
        self.assertNotEqual(item_before_update.updated_at, item_dict.get("updated_at"))

    async def test_update_item_with_non_existing_id(self) -> None:
        """Test updating an item with a non-existing id."""
        with self.assertRaises(ItemDoesNotExist):
            await item_service.update_item(item_id=999)
