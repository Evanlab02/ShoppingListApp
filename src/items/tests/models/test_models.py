"""Test item app models."""

from django.contrib.auth.models import User
from django.test import TestCase

from items.models import ShoppingItem
from stores.models import ShoppingStore as Store


class TestItemsApp(TestCase):
    """Test the items app."""

    async def test_item_model_to_string(self) -> None:
        """Test the item model to string method."""
        user = await User.objects.acreate(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )

        store = await Store.objects.acreate(
            name="Test Store",
            store_type=1,
            description="",
            user=user,
        )

        item = await ShoppingItem.objects.acreate(
            name="My Test Item",
            price=100,
            description="",
            user=user,
            store=store,
        )

        self.assertEqual(str(item), "My Test Item@Test Store")
