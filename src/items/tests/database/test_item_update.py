"""Contains tests for the item repo update functions."""

from items.database import item_repo
from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestUpdateItem(BaseTestCase):
    """Test the item repo update functions."""

    async def test_update_item_with_no_changes(self) -> None:
        """Test updating an item with no changes."""
        # Get item before update
        item_before_update = await Item.objects.select_related("user", "store").aget(
            id=self.item.id
        )

        # Update the item
        item = await item_repo.update_item(item_id=self.item.id, user=self.user)

        # Item ID remains the same
        self.assertEqual(item.id, item_before_update.id)

        # No values are changed due to no values being passed
        self.assertEqual(item.name, item_before_update.name)
        self.assertEqual(item.price, item_before_update.price)
        self.assertEqual(item.description, item_before_update.description)

        # Created at always remains the same
        self.assertEqual(item.created_at.isoformat(), item_before_update.created_at.isoformat())

        # Updated at should have changed
        self.assertNotEqual(item.updated_at.isoformat(), self.item.updated_at.isoformat())

        # Check that related models are not changed
        self.assertEqual(item.store, item_before_update.store)
        self.assertEqual(item.user, item_before_update.user)

    async def test_update_item_name(self) -> None:
        """Test updating an item's name."""
        new_name = "New Name"

        # Update the item
        item = await item_repo.update_item(item_id=self.item.id, user=self.user, name=new_name)

        self.assertEqual(item.id, self.item.id)  # Item ID remains the same
        self.assertEqual(item.name, new_name)  # Check that the name is updated
        self.assertNotEqual(
            item.updated_at.isoformat(), self.item.updated_at.isoformat()
        )  # Updated at should have changed

    async def test_update_item_price(self) -> None:
        """Test updating an item's price."""
        new_price = 100.0

        # Update the item
        item = await item_repo.update_item(item_id=self.item.id, user=self.user, price=new_price)

        self.assertEqual(item.id, self.item.id)  # Item ID remains the same
        self.assertEqual(item.price, new_price)  # Check that the price is updated
        self.assertNotEqual(
            item.updated_at.isoformat(), self.item.updated_at.isoformat()
        )  # Updated at should have changed

    async def test_update_item_description(self) -> None:
        """Test updating an item's description."""
        new_description = "ABCD"

        # Update the item
        item = await item_repo.update_item(
            item_id=self.item.id, user=self.user, description=new_description
        )

        self.assertEqual(item.id, self.item.id)  # Item ID remains the same
        self.assertEqual(item.description, new_description)  # Check that the description is updated
        self.assertNotEqual(
            item.updated_at.isoformat(), self.item.updated_at.isoformat()
        )  # Updated at should have changed

    async def test_update_item_store(self) -> None:
        """Test updating an item's store."""
        # Create a temporary store
        temp_store = await self.create_temporary_store()

        # Update the item
        item = await item_repo.update_item(item_id=self.item.id, user=self.user, store=temp_store)

        self.assertEqual(item.id, self.item.id)
        self.assertEqual(item.store, temp_store)
        self.assertNotEqual(item.updated_at.isoformat(), self.item.updated_at.isoformat())

    async def test_update_item_with_invalid_id(self) -> None:
        """Test updating an item with an invalid ID."""
        with self.assertRaises(Item.DoesNotExist):
            await item_repo.update_item(item_id=99999, user=self.user)

    async def test_update_with_invalid_user(self) -> None:
        """Test updating an item with an invalid user."""
        # Create a temporary user
        temp_user = await self.create_temporary_user()

        with self.assertRaises(Item.DoesNotExist):
            await item_repo.update_item(item_id=self.item.id, user=temp_user)
