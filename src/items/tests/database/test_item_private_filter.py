"""Contains tests for the _filter function of the item repository."""

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


class TestFilterItems(TestCase):
    """Test the item repository _filter function."""

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

    async def test_no_filter(self) -> None:
        """Test the _filter function with no filters."""
        records = await item_repo._filter()
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_item_name_is_equal(self) -> None:
        """Test the _filter function with a name filter."""
        records = await item_repo._filter(name="Test Item")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

    async def test_filter_item_name_contains(self) -> None:
        """Test the _filter function with a name filter."""
        records = await item_repo._filter(name="Test")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

    async def test_filter_item_name_is_not_equal(self) -> None:
        """Test the _filter function with a name filter."""
        records = await item_repo._filter(name="Not Test Item")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_item_name_both(self) -> None:
        """Test the _filter function with a name filter."""
        records = await item_repo._filter(name="Item")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_item_description_is_equal(self) -> None:
        """Test the _filter function with a description filter."""
        records = await item_repo._filter(description="Test Description")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Test Description")

    async def test_filter_item_description_contains(self) -> None:
        """Test the _filter function with a description filter."""
        records = await item_repo._filter(description="Test")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Test Description")

    async def test_filter_item_description_is_not_equal(self) -> None:
        """Test the _filter function with a description filter."""
        records = await item_repo._filter(description="Not Test Description")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_item_description_both(self) -> None:
        """Test the _filter function with a description filter."""
        records = await item_repo._filter(description="Description")
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_price_is_equal(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is=100)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 100)

    async def test_filter_price_is_not_equal(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is=50)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_price_is_greater_than(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_gt=50)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_price_is_greater_than_does_not_include(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_gt=100)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 200)

    async def test_filter_price_is_greater_than_none(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_gt=200)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_price_is_less_than(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_lt=250)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_price_is_less_than_does_not_include(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_lt=200)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 100)

    async def test_filter_price_is_less_than_none(self) -> None:
        """Test the _filter function with a price filter."""
        records = await item_repo._filter(price_is_lt=100)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_created_on(self) -> None:
        """Test the _filter function with a created_on filter."""
        records = await item_repo._filter(created_on=self.item.created_at.date())
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_created_on_none(self) -> None:
        """Test the _filter function with a created_on filter."""
        records = await item_repo._filter(created_on=date(2020, 1, 1))
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_created_after(self) -> None:
        """Test the _filter function with a created_after filter."""
        records = await item_repo._filter(
            created_after=self.item.created_at.date() - timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_created_after_none(self) -> None:
        """Test the _filter function with a created_after filter."""
        records = await item_repo._filter(
            created_after=self.item.created_at.date() + timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_created_before(self) -> None:
        """Test the _filter function with a created_before filter."""
        records = await item_repo._filter(
            created_before=self.item.created_at.date() + timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_created_before_none(self) -> None:
        """Test the _filter function with a created_before filter."""
        records = await item_repo._filter(
            created_before=self.item.created_at.date() - timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_updated_on(self) -> None:
        """Test the _filter function with a updated_on filter."""
        records = await item_repo._filter(updated_on=self.item.updated_at.date())
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_updated_on_none(self) -> None:
        """Test the _filter function with a updated_on filter."""
        records = await item_repo._filter(updated_on=date(2020, 1, 1))
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_updated_after(self) -> None:
        """Test the _filter function with a updated_after filter."""
        records = await item_repo._filter(
            updated_after=self.item.updated_at.date() - timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_updated_after_none(self) -> None:
        """Test the _filter function with a updated_after filter."""
        records = await item_repo._filter(
            updated_after=self.item.updated_at.date() + timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_updated_before(self) -> None:
        """Test the _filter function with a updated_before filter."""
        records = await item_repo._filter(
            updated_before=self.item.updated_at.date() + timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_updated_before_none(self) -> None:
        """Test the _filter function with a updated_before filter."""
        records = await item_repo._filter(
            updated_before=self.item.updated_at.date() - timedelta(days=1)
        )
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_store(self) -> None:
        """Test the _filter function with a store filter."""
        records = await item_repo._filter(store=self.store)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_store_none(self) -> None:
        """Test the _filter function with a store filter."""
        test_store = await Store.objects.acreate(
            name="Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        await test_store.asave()
        records = await item_repo._filter(store=test_store)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    async def test_filter_user(self) -> None:
        """Test the _filter function with a user filter."""
        records = await item_repo._filter(user=self.user)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    async def test_filter_user_none(self) -> None:
        """Test the _filter function with a user filter."""
        test_user = await User.objects.acreate(
            username="testuser2",
            email="testuser2@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        await test_user.asave()
        records = await item_repo._filter(user=test_user)
        items = [record async for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)
