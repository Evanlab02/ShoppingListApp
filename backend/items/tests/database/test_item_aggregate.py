"""Contains tests for the aggregate function of the item repository."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestItemRepositoryAggregate(TestCase):
    """Test the aggregate function of the item repository."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        self.item = ItemFactory.create_batch(size=3, user=self.user, store=self.store)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_aggregate(self) -> None:
        """Test the aggregate function of the item repository."""
        all_items = Item.objects.all()
        total_price = sum([item.price async for item in all_items])
        average_price = total_price / 3
        max_price = max([item.price async for item in all_items])
        min_price = min([item.price async for item in all_items])

        aggregate = await self.repo.aggregate(self.user)
        self.assertEqual(aggregate["total_items"], 3)
        self.assertEqual(aggregate["total_price"], total_price)
        self.assertEqual(aggregate["average_price"], average_price)
        self.assertEqual(aggregate["max_price"], max_price)
        self.assertEqual(aggregate["min_price"], min_price)
