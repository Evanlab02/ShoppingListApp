"""Contains tests for the _filter function of the item repository."""

from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
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

    def test_no_filter(self) -> None:
        """Test the _filter function with no filters."""
        records = item_repo._filter()
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_item_name_is_equal(self) -> None:
        """Test the _filter function with a name filter."""
        records = item_repo._filter(name="Test Item")
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

    def test_filter_item_name_contains(self) -> None:
        """Test the _filter function with a name filter."""
        records = item_repo._filter(name="Test")
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Test Item")

    def test_filter_item_name_is_not_equal(self) -> None:
        """Test the _filter function with a name filter."""
        records = item_repo._filter(name="Not Test Item")
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_item_name_both(self) -> None:
        """Test the _filter function with a name filter."""
        records = item_repo._filter(name="Item")
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_item_description_is_equal(self) -> None:
        """Test the _filter function with a description filter."""
        search = ItemSearchSchema(description="Test Description")
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Test Description")

    def test_filter_item_description_contains(self) -> None:
        """Test the _filter function with a description filter."""
        search = ItemSearchSchema(description="Test")
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].description, "Test Description")

    def test_filter_item_description_is_not_equal(self) -> None:
        """Test the _filter function with a description filter."""
        search = ItemSearchSchema(description="Not Test Description")
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_item_description_both(self) -> None:
        """Test the _filter function with a description filter."""
        search = ItemSearchSchema(description="Description")
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_price_is_equal(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price=100)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 100)

    def test_filter_price_is_not_equal(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price=50)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_price_is_greater_than(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_gt=50)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_price_is_greater_than_does_not_include(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_gt=100)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 200)

    def test_filter_price_is_greater_than_none(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_gt=200)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_price_is_less_than(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_lt=250)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_price_is_less_than_does_not_include(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_lt=200)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].price, 100)

    def test_filter_price_is_less_than_none(self) -> None:
        """Test the _filter function with a price filter."""
        search = ItemSearchSchema(price_is_lt=100)
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_created_on(self) -> None:
        """Test the _filter function with a created_on filter."""
        search = ItemSearchSchema(created_on=self.item.created_at.date())
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_created_on_none(self) -> None:
        """Test the _filter function with a created_on filter."""
        search = ItemSearchSchema(created_on=date(2020, 1, 1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_created_after(self) -> None:
        """Test the _filter function with a created_after filter."""
        search = ItemSearchSchema(created_after=self.item.created_at.date() - timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_created_after_none(self) -> None:
        """Test the _filter function with a created_after filter."""
        search = ItemSearchSchema(created_after=self.item.created_at.date() + timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_created_before(self) -> None:
        """Test the _filter function with a created_before filter."""
        search = ItemSearchSchema(created_before=self.item.created_at.date() + timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_created_before_none(self) -> None:
        """Test the _filter function with a created_before filter."""
        search = ItemSearchSchema(created_before=self.item.created_at.date() - timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_updated_on(self) -> None:
        """Test the _filter function with a updated_on filter."""
        search = ItemSearchSchema(updated_on=self.item.updated_at.date())
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_updated_on_none(self) -> None:
        """Test the _filter function with a updated_on filter."""
        search = ItemSearchSchema(updated_on=date(2020, 1, 1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_updated_after(self) -> None:
        """Test the _filter function with a updated_after filter."""
        search = ItemSearchSchema(updated_after=self.item.updated_at.date() - timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_updated_after_none(self) -> None:
        """Test the _filter function with a updated_after filter."""
        search = ItemSearchSchema(updated_after=self.item.updated_at.date() + timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_updated_before(self) -> None:
        """Test the _filter function with a updated_before filter."""
        search = ItemSearchSchema(updated_before=self.item.updated_at.date() + timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_updated_before_none(self) -> None:
        """Test the _filter function with a updated_before filter."""
        search = ItemSearchSchema(updated_before=self.item.updated_at.date() - timedelta(days=1))
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_store(self) -> None:
        """Test the _filter function with a store filter."""
        records = item_repo._filter(store=self.store)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_store_none(self) -> None:
        """Test the _filter function with a store filter."""
        test_store = Store.objects.create(
            name="Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        test_store.save()
        records = item_repo._filter(store=test_store)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_user(self) -> None:
        """Test the _filter function with a user filter."""
        records = item_repo._filter(user=self.user)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_user_none(self) -> None:
        """Test the _filter function with a user filter."""
        test_user = User.objects.create(
            username="testuser2",
            email="testuser2@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        test_user.save()
        records = item_repo._filter(user=test_user)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)

    def test_filter_item_ids(self) -> None:
        """Test the _filter function with ids filter."""
        search = ItemSearchSchema(ids=[self.item.id])
        records = item_repo._filter(search=search)
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 1)

        item = items[0]
        self.assertEqual(item.name, self.item.name)

    def test_filter_item_stores(self) -> None:
        """Test the filter with stores."""
        records = item_repo._filter(stores=[self.store])
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 2)

    def test_filter_item_stores_with_no_items(self) -> None:
        """Test the filter with a store that has no items."""
        self.store = Store.objects.create(
            name="No Items Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        records = item_repo._filter(stores=[self.store])
        items = [record for record in records]
        self.assertIsInstance(items, list)
        self.assertEqual(len(items), 0)
