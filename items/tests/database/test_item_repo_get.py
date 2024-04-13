"""Contains tests for the item repo get functions."""

import pytest

from items.database import item_repo
from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestGetItemByIds(BaseTestCase):
    """Test the item repo get functions."""

    async def get_item_by_id(self) -> None:
        """Test getting an item by its id."""
        item = await item_repo.get_item(item_id=self.item.id)
        self.assertEqual(item.id, self.item.id)
        self.assertEqual(item.name, self.item.name)
        self.assertEqual(item.description, self.item.description)
        self.assertEqual(item.price, self.item.price)
        self.assertEqual(item.created_at, self.item.created_at)
        self.assertEqual(item.updated_at, self.item.updated_at)

    async def test_get_item_by_id_that_does_not_exist(self) -> None:
        """Test getting an item by its id that does not exist."""
        with pytest.raises(Item.DoesNotExist):
            await item_repo.get_item(item_id=100)
