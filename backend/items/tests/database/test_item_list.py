"""Contains tests for the search function of the item repository."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory

MOCK_NAME = "Test Item"
MOCK_DESRIPTION = "Test Description"


class TestItemRepositorySearch(TestCase):
    """Test the item repository search function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        self.schema = ItemSearchSchema(
            description=None,
            price=None,
            price_is_lt=None,
            price_is_gt=None,
            created_on=None,
            created_before=None,
            created_after=None,
            updated_on=None,
            updated_before=None,
            updated_after=None,
            ids=None,
            stores=None,
        )
        self.create_item = sync_to_async(ItemFactory.create)
        self.create_batch = sync_to_async(ItemFactory.create_batch)
        self.create_store = sync_to_async(StoreFactory.create)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Store.objects.all().delete()
        Item.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_get_items(self) -> None:
        """Test the search by description function."""
        await self.create_batch(size=100, user=self.user, store=self.store)

        items = await self.repo.get_items()
        self.assertEqual(items.total, 100)

        for item in items.items:
            self.assertEqual(item.user.username, self.user.username)  # type: ignore
            self.assertEqual(item.store.name, self.store.name)  # type: ignore

    async def test_get_items_with_description(self) -> None:
        """Test the search by description function."""
        self.schema.description = MOCK_DESRIPTION
        await self.create_item(user=self.user, store=self.store, description=MOCK_DESRIPTION)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("description", None), MOCK_DESRIPTION)

    async def test_get_items_with_price(self) -> None:
        """Test the search by price function."""
        self.schema.price = "100.00"
        await self.create_item(user=self.user, store=self.store, price=100)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("price", None), 100)

    async def test_get_items_with_price_is_gt(self) -> None:
        """Test the search by price greater than function."""
        self.schema.price_is_gt = 50.00
        await self.create_item(user=self.user, store=self.store, price=100)
        await self.create_item(user=self.user, store=self.store, price=25)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("price", None), 100)

    async def test_get_items_with_price_is_lt(self) -> None:
        """Test the search by price less than function."""
        self.schema.price_is_lt = 50.00
        await self.create_item(user=self.user, store=self.store, price=25)
        await self.create_item(user=self.user, store=self.store, price=100)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("price", None), 25)

    async def test_get_items_with_created_on(self) -> None:
        """Test the search by creation date function."""
        from datetime import date

        today = date.today()
        self.schema.created_on = today
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_created_after(self) -> None:
        """Test the search by creation date after function."""
        from datetime import date, timedelta

        yesterday = date.today() - timedelta(days=1)
        self.schema.created_after = yesterday
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_created_before(self) -> None:
        """Test the search by creation date before function."""
        from datetime import date, timedelta

        tomorrow = date.today() + timedelta(days=1)
        self.schema.created_before = tomorrow
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_updated_on(self) -> None:
        """Test the search by update date function."""
        from datetime import date

        today = date.today()
        self.schema.updated_on = today
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_updated_after(self) -> None:
        """Test the search by update date after function."""
        from datetime import date, timedelta

        yesterday = date.today() - timedelta(days=1)
        self.schema.updated_after = yesterday
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_updated_before(self) -> None:
        """Test the search by update date before function."""
        from datetime import date, timedelta

        tomorrow = date.today() + timedelta(days=1)
        self.schema.updated_before = tomorrow
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)

    async def test_get_items_with_ids(self) -> None:
        """Test the search by item IDs function."""
        items_to_search = await self.create_batch(size=3, user=self.user, store=self.store)
        self.schema.ids = [items_to_search[0].id, items_to_search[1].id]

        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 2)

    async def test_get_items_with_stores(self) -> None:
        """Test the search by stores function."""
        store2 = await self.create_store(user=self.user)
        await self.create_item(user=self.user, store=self.store)
        await self.create_item(user=self.user, store=store2)

        self.schema.stores = [self.store.id]
        items = await self.repo.get_items(search=self.schema)
        self.assertEqual(items.total, 1)
        self.assertEqual(items.items[0].store.id, self.store.id)  # type: ignore

    async def test_get_items_for_name(self) -> None:
        """Test the search by name function."""
        await self.create_item(user=self.user, store=self.store, name=MOCK_NAME)
        await self.create_item(
            user=self.user,
            store=self.store,
            name="Very Very Long Random Name That Is Not The Same As The Mock Name",
        )

        items = await self.repo.get_items(name=MOCK_NAME)
        self.assertEqual(items.total, 1)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("name", None), MOCK_NAME)

    async def test_get_items_for_store(self) -> None:
        """Test the search by store function."""
        await self.create_item(user=self.user, store=self.store)
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(store=self.store.id)
        self.assertEqual(items.total, 2)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("store", None).get("id"), self.store.id)

    async def test_get_items_for_user(self) -> None:
        """Test the search by user function."""
        await self.create_item(user=self.user, store=self.store)
        await self.create_item(user=self.user, store=self.store)

        items = await self.repo.get_items(user=self.user)
        self.assertEqual(items.total, 2)

        result = items.items[0].model_dump()
        self.assertEqual(result.get("user", None).get("username"), self.user.username)

    async def test_paginate_out_of_bounds(self) -> None:
        """Test the paginate out of bounds function."""
        await self.create_batch(size=100, user=self.user, store=self.store)

        items = await self.repo.get_items(page=200, items_per_page=10)
        self.assertEqual(items.total, 100)
        self.assertEqual(items.total_pages, 10)
        self.assertEqual(items.page_number, 10)
        self.assertEqual(items.has_previous, True)
        self.assertEqual(items.previous_page, 9)
        self.assertEqual(items.has_next, False)
        self.assertEqual(items.next_page, None)
