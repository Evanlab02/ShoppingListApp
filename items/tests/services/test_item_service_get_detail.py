"""Contains tests for the item service get detail function."""

from items.errors.exceptions import ItemDoesNotExist
from items.services import item_service
from items.tests.base.base_test_case import BaseTestCase


class TestGetItemDetails(BaseTestCase):
    """Test the item service get detail function."""

    async def test_get_item_details(self) -> None:
        """Test that the item details are retrieved."""
        item = await item_service.get_item_detail(item_id=self.item.id)
        item_dict = item.model_dump()
        self.assertEqual(item_dict["name"], self.item.name)
        self.assertEqual(item_dict["description"], self.item.description)
        self.assertEqual(item_dict["price"], 100.00)
        self.assertEqual(item_dict["created_at"], self.item.created_at)
        self.assertEqual(item_dict["updated_at"], self.item.updated_at)

        self.assertEqual(item_dict["store"]["id"], self.store.id)
        self.assertEqual(item_dict["store"]["name"], self.store.name)

        self.assertEqual(item_dict["user"]["username"], self.user.username)

    async def test_get_item_details_invalid_item_id(self) -> None:
        """Test that an invalid item id raises an exception."""
        with self.assertRaises(ItemDoesNotExist):
            await item_service.get_item_detail(item_id=99999)
