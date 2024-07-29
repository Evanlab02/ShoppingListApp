"""Contains tests for the _paginate function of the item repository."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


class TestPaginateItems(TestCase):
    """Test the item repository _paginate function."""

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

        self.alt_store = Store.objects.create(
            name="Alternate Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.alt_store.save()

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

        self.alt_store_item = Item.objects.create(
            name="Alternate Store Item",
            description="Alternate Store Description",
            price=300,
            store=self.alt_store,
            user=self.user,
        )
        self.alt_store_item.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    async def test_paginate_items(self) -> None:
        """Test that items are paginated."""
        items = await item_repo._paginate()
        self.assertEqual(len(items.items), 3)
        self.assertEqual(items.total, 3)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_paginate_items_page_1(self) -> None:
        """Test that items are paginated on page 1 with 1 item per page."""
        items = await item_repo._paginate(items_per_page=1)
        self.assertEqual(len(items.items), 1)
        self.assertEqual(items.total, 3)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 3)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, True)
        self.assertIsNone(items.previous_page)
        self.assertIsNotNone(items.next_page)

    async def test_paginate_items_page_2(self) -> None:
        """Test that items are paginated on page 2 with 1 item per page."""
        items = await item_repo._paginate(items_per_page=1, page_number=2)
        self.assertEqual(len(items.items), 1)
        self.assertEqual(items.total, 3)
        self.assertEqual(items.page_number, 2)
        self.assertEqual(items.total_pages, 3)
        self.assertEqual(items.has_previous, True)
        self.assertEqual(items.has_next, True)
        self.assertIsNotNone(items.previous_page)
        self.assertIsNotNone(items.next_page)

    async def test_paginate_items_with_user(self) -> None:
        """Test that items are paginated with a user."""
        items = await item_repo._paginate(user=self.user)
        self.assertEqual(len(items.items), 3)
        self.assertEqual(items.total, 3)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_paginate_items_no_items_user(self) -> None:
        """Test that items are paginated with a user that has no items."""
        new_user = await User.objects.acreate(
            username="newuser",
            email="newuser@gmail.com",
            password="newpass",
            first_name="New",
            last_name="User",
        )
        await new_user.asave()

        items = await item_repo._paginate(user=new_user)
        self.assertEqual(len(items.items), 0)
        self.assertEqual(items.total, 0)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_paginate_items_with_store(self) -> None:
        """Test that items are paginated with a store."""
        items = await item_repo._paginate(store=self.store)
        self.assertEqual(len(items.items), 2)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

        items = await item_repo._paginate(store=self.alt_store)
        self.assertEqual(len(items.items), 1)
        self.assertEqual(items.total, 1)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)
