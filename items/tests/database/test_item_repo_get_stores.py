"""Contains tests for the get_items function of the item repository."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


class TestGetItems(TestCase):
    """Test the item repository get_items function."""

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
            name="Test Item",
            description="Test Description",
            price=100,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        self.alt_item = Item.objects.create(
            name="Alternate Item",
            description="Alternate Description",
            price=200,
            store=self.store,
            user=self.user,
        )
        self.alt_item.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    async def test_get_items(self) -> None:
        """Test getting all items."""
        items = await item_repo.get_items()
        self.assertEqual(len(items.items), 2)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_paginate_items_page_1(self) -> None:
        """Test that items are paginated on page 1 with 1 item per page."""
        items = await item_repo.get_items(items_per_page=1)
        self.assertEqual(len(items.items), 1)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 2)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, True)
        self.assertIsNone(items.previous_page)
        self.assertIsNotNone(items.next_page)

    async def test_paginate_items_page_2(self) -> None:
        """Test that items are paginated on page 2 with 1 item per page."""
        items = await item_repo.get_items(items_per_page=1, page=2)
        self.assertEqual(len(items.items), 1)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 2)
        self.assertEqual(items.total_pages, 2)
        self.assertEqual(items.has_previous, True)
        self.assertEqual(items.has_next, False)
        self.assertIsNotNone(items.previous_page)
        self.assertIsNone(items.next_page)
