"""Contains tests for the item repo update functions."""

from items.database import item_repo
from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestUpdateItem(BaseTestCase):
    """Test the item repo update functions."""

    async def test_update_item(self) -> None:
        """Test updating an item."""
        # Get item before update
        item_before_update = await Item.objects.aget(id=self.item.id)

        # Update the item
        item = await item_repo.update_item(item_id=self.item.id)

        # Item ID remains the same
        self.assertEqual(item.id, item_before_update.id)

        # No values are changed due to no values being passed
        self.assertEqual(item.name, item_before_update.name)
        self.assertEqual(item.price, item_before_update.price)
        self.assertEqual(item.description, item_before_update.description)

        # Created at always remains the same
        self.assertEqual(item.created_at.isoformat(), item_before_update.created_at.isoformat())

        # Updated at should be the same as there was no actual update
        self.assertEqual(item.updated_at.isoformat(), item_before_update.updated_at.isoformat())

        # TODO: Check that related models are not changed
