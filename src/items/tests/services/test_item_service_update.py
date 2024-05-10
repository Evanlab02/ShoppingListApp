"""Contains tests for the item service update function."""

from items.errors.exceptions import ItemDoesNotExist, ItemAlreadyExists
from items.models import ShoppingItem as Item
from items.services import item_service
from items.tests.base.base_test_case import BaseTestCase
from stores.errors.api_exceptions import StoreDoesNotExist


class TestUpdateItemService(BaseTestCase):
    """Test the item service update function."""

    async def test_update_item_with_no_changes(self) -> None:
        """Test updating an item with no changes."""
        item_before_update = await Item.objects.aget(id=self.item.id)
        item = await item_service.update_item(item_id=self.item.id, user=self.user)
        item_dict = item.model_dump()

        self.assertEqual(item_before_update.id, item_dict.get("id"))  # ID remains the same
        self.assertEqual(item_before_update.name, item_dict.get("name"))  # Name remains the same
        self.assertEqual(item_before_update.price, item_dict.get("price"))  # Price remains the same

        # Updated at changes
        self.assertNotEqual(item_before_update.updated_at, item_dict.get("updated_at"))

    async def test_update_item_with_non_existing_id(self) -> None:
        """Test updating an item with a non-existing id."""
        with self.assertRaises(ItemDoesNotExist):
            await item_service.update_item(item_id=999, user=self.user)

    async def test_update_item(self) -> None:
        """Test updating an item."""
        new_store = await self.create_temporary_store()
        new_name = "Testing Update Name"
        new_price = 100.0
        new_description = "New Description"
        new_store_id = new_store.id

        item_before_update = await Item.objects.aget(id=self.item.id)
        item = await item_service.update_item(
            item_id=self.item.id,
            user=self.user,
            name=new_name,
            price=new_price,
            description=new_description,
            store_id=new_store_id,
        )
        item_dict = item.model_dump()

        self.assertEqual(item_before_update.id, item_dict.get("id"))  # ID remains the same
        self.assertEqual(new_name, item_dict.get("name"))
        self.assertEqual(new_price, item_dict.get("price"))
        self.assertEqual(new_description, item_dict.get("description"))
        self.assertEqual(new_store_id, item_dict.get("store", {"id": 0}).get("id"))

    async def test_update_item_with_invalid_store_id(self) -> None:
        """Test updating an item with an invalid store id."""
        with self.assertRaises(StoreDoesNotExist):
            await item_service.update_item(item_id=self.item.id, user=self.user, store_id=999)

    async def test_update_item_with_duplicate_name_and_store(self) -> None:
        """Test updating an item with a duplicate name and store."""
        new_store = await self.create_temporary_store()
        new_item = await self.create_temporary_item(store=new_store)

        with self.assertRaises(ItemAlreadyExists):
            await item_service.update_item(
                item_id=self.item.id, user=self.user, name=new_item.name, store_id=new_store.id
            )

    async def test_update_item_with_duplicate_name_and_same_store(self) -> None:
        """Test updating an item with a duplicate name and same store."""
        new_store = await self.create_temporary_store()
        new_item = await self.create_temporary_item(store=new_store)

        with self.assertRaises(ItemAlreadyExists):
            await item_service.update_item(
                item_id=new_item.id,
                user=self.user,
                name=new_item.name,
            )
