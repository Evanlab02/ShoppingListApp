"""Contains tests for the delete_item function of the item repository."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestItemRepositoryDelete(TestCase):
    """Test the item repository delete_item function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        self.item = ItemFactory.create(
            user=self.user,
            store=self.store,
            name="Test Item",
            description="Test Description",
            price=10.0,
        )
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Store.objects.all().delete()
        Item.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_delete_item(self) -> None:
        """Test deleting an item."""
        # Delete the item
        await self.repo.delete_item(self.item.id, self.user)

        # Verify the item no longer exists
        with self.assertRaises(Item.DoesNotExist):
            await Item.objects.aget(id=self.item.id)

    async def test_delete_item_wrong_user(self) -> None:
        """Test deleting an item with wrong user raises DoesNotExist."""
        other_user = await sync_to_async(UserFactory.create)()

        # Attempt to delete with wrong user should raise DoesNotExist
        with self.assertRaises(Item.DoesNotExist):
            await self.repo.delete_item(self.item.id, other_user)

        # Verify item still exists
        item = await Item.objects.aget(id=self.item.id)
        self.assertEqual(item.id, self.item.id)

    async def test_delete_nonexistent_item(self) -> None:
        """Test deleting a non-existent item raises DoesNotExist."""
        non_existent_id = 99999

        with self.assertRaises(Item.DoesNotExist):
            await self.repo.delete_item(non_existent_id, self.user)
