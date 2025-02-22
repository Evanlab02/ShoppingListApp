"""Tests for the item update service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.errors.api_exceptions import StoreDoesNotExist
from stores.tests.factory import StoreFactory


class ItemUpdateServiceTestCase(TestCase):
    """Tests for the item update service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create()
        self.item = ItemFactory.create()

    async def test_update_item_store_to_one_that_does_not_exist(self) -> None:
        """Test the update item method when the store does not exist."""
        with self.assertRaises(StoreDoesNotExist):
            await self.item_service.update_item(
                item_id=self.item.id,
                user=self.user,
                new_store_id=99999,
            )
