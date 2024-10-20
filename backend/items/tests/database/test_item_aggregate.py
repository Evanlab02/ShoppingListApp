"""Contains tests for the aggregate function of the item repository."""

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
        Item.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_aggregate_items(self) -> None:
        """Test the aggregate items function."""
        aggregate = await item_repo.aggregate()

        total_items = aggregate.get("total_items")
        self.assertEqual(total_items, 2)

        total_price = aggregate.get("total_price")
        self.assertEqual(total_price, 300)

        average_price = aggregate.get("average_price")
        self.assertEqual(average_price, 150)

        max_price = aggregate.get("max_price")
        self.assertEqual(max_price, 200)

        min_price = aggregate.get("min_price")
        self.assertEqual(min_price, 100)

    async def test_aggregate_items_with_user(self) -> None:
        """Test the aggregate items function with a user."""
        aggregate = await item_repo.aggregate(user=self.user)

        total_items = aggregate.get("total_items")
        self.assertEqual(total_items, 2)

        total_price = aggregate.get("total_price")
        self.assertEqual(total_price, 300)

        average_price = aggregate.get("average_price")
        self.assertEqual(average_price, 150)

        max_price = aggregate.get("max_price")
        self.assertEqual(max_price, 200)

        min_price = aggregate.get("min_price")
        self.assertEqual(min_price, 100)

    async def test_aggregate_with_user_no_items(self) -> None:
        """Test the aggregate items function with a user and no items."""
        new_user = await User.objects.acreate(
            username="newuser",
            email="newuser@gmail.com",
            password="newpass",
            first_name="New",
            last_name="User",
        )
        await new_user.asave()

        aggregate = await item_repo.aggregate(user=new_user)

        total_items = aggregate.get("total_items")
        self.assertEqual(total_items, 0)

        total_price = aggregate.get("total_price")
        self.assertEqual(total_price, None)

        average_price = aggregate.get("average_price")
        self.assertEqual(average_price, None)

        max_price = aggregate.get("max_price")
        self.assertEqual(max_price, None)

        min_price = aggregate.get("min_price")
        self.assertEqual(min_price, None)

    async def test_aggregate_items_with_no_items(self) -> None:
        """Test the aggregate items function with no items."""
        await Item.objects.all().adelete()

        aggregate = await item_repo.aggregate()

        total_items = aggregate.get("total_items")
        self.assertEqual(total_items, 0)

        total_price = aggregate.get("total_price")
        self.assertEqual(total_price, None)

        average_price = aggregate.get("average_price")
        self.assertEqual(average_price, None)

        max_price = aggregate.get("max_price")
        self.assertEqual(max_price, None)

        min_price = aggregate.get("min_price")
        self.assertEqual(min_price, None)
