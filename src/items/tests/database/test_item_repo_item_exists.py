"""Test the item repo item exists function."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

MOCK_ITEM_NAME = "Logitech G Pro X"


class TestItemRepositoryItemExists(TestCase):
    """Test the item repo item exists function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        self.store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        self.item = Item.objects.create(
            name=MOCK_ITEM_NAME,
            description="",
            price=2500,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    async def test_item_does_exist(self) -> None:
        """Test that does item exists function returns true."""
        exists = await item_repo.does_item_exist(MOCK_ITEM_NAME, self.store)
        self.assertTrue(exists)

    async def test_item_does_not_exist(self) -> None:
        """Test that does item exists function returns false."""
        exists = await item_repo.does_item_exist("Logitech MX Keys Mini", self.store)
        self.assertFalse(exists)
