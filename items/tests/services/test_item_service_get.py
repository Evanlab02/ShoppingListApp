"""Contains tests for the item service get_items function."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.models import ShoppingItem as Item
from items.services import item_service
from stores.models import ShoppingStore as Store


class TestItemServiceGetItems(TestCase):
    """Test the store service get items."""

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
        items = await item_service.get_items()
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertEqual(len(items.items), 2)

    async def test_get_items_pagination_page_1(self) -> None:
        """Test getting all items with pagination."""
        items = await item_service.get_items(page=1, items_per_page=1)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 2)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, True)
        self.assertEqual(len(items.items), 1)

    async def test_get_items_pagination_page_2(self) -> None:
        """Test getting all items with pagination."""
        items = await item_service.get_items(page=2, items_per_page=1)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 2)
        self.assertEqual(items.total_pages, 2)
        self.assertEqual(items.has_previous, True)
        self.assertEqual(items.has_next, False)
        self.assertEqual(len(items.items), 1)

    async def test_get_items_personal(self) -> None:
        """Test getting all items for a user."""
        items = await item_service.get_items(user=self.user)
        self.assertEqual(len(items.items), 2)
        self.assertEqual(items.total, 2)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)

    async def test_get_items_no_items_user(self) -> None:
        """Test getting all items for a user with no items."""
        new_user = await User.objects.acreate(
            username="newuser",
            email="newuser@gmail.com",
            password="newpass",
            first_name="New",
            last_name="User",
        )
        await new_user.asave()

        items = await item_service.get_items(user=new_user)
        self.assertEqual(len(items.items), 0)
        self.assertEqual(items.total, 0)
        self.assertEqual(items.page_number, 1)
        self.assertEqual(items.total_pages, 1)
        self.assertEqual(items.has_previous, False)
        self.assertEqual(items.has_next, False)
        self.assertIsNone(items.previous_page)
        self.assertIsNone(items.next_page)
