"""Test the store search functionality."""

from datetime import date, timedelta

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.models import ShoppingStore as Store
from stores.schemas.input import StoreSearch
from stores.tests.factory import StoreFactory


class TestStoreSearch(TestCase):
    """Test the store search functionality."""

    def setUp(self) -> None:
        """Set up the test."""
        self.repo = StoreRepo()
        self.stores = StoreFactory.create_batch(50)
        self.acreate = sync_to_async(StoreFactory.create)
        self.acreate_batch = sync_to_async(StoreFactory.create_batch)
        self.acreate_user = sync_to_async(UserFactory.create)
        self.search = StoreSearch(
            ids=None,
            store_types=None,
            created_on=None,
            created_before=None,
            created_after=None,
            updated_on=None,
            updated_before=None,
            updated_after=None,
        )
        return super().setUp()

    async def test_search_stores_by_name(self) -> None:
        """Test the search stores by name functionality."""
        for i in range(50):
            await self.acreate(name=f"Test Store {i}")

        stores = await self.repo.search_stores(name="Test Store", sort="name", sort_dir="asc")

        self.assertEqual(stores.total, 50)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 5)
        self.assertEqual(len(stores.stores), 10)

        self.assertEqual(stores.next_page, 2)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.has_previous, False)

        store_0 = stores.stores[0].model_dump()
        store_1 = stores.stores[1].model_dump()
        store_2 = stores.stores[2].model_dump()

        self.assertEqual(store_0.get("name"), "Test Store 0")
        self.assertEqual(store_1.get("name"), "Test Store 1")
        self.assertEqual(store_2.get("name"), "Test Store 10")

    async def test_search_stores_by_user(self) -> None:
        """Test the search stores by user functionality."""
        user = await self.acreate_user()
        await self.acreate_batch(50, user=user)
        stores = await self.repo.search_stores(user=user)

        self.assertEqual(stores.total, 50)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 5)
        self.assertEqual(len(stores.stores), 10)

        self.assertEqual(stores.next_page, 2)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.has_previous, False)

        store_0 = stores.stores[0].model_dump()
        store_1 = stores.stores[1].model_dump()
        store_2 = stores.stores[2].model_dump()

        self.assertEqual(store_0.get("user", {}).get("username"), user.username)
        self.assertEqual(store_1.get("user", {}).get("username"), user.username)
        self.assertEqual(store_2.get("user", {}).get("username"), user.username)

    async def test_search_stores_by_ids(self) -> None:
        """Test the search stores by ids functionality."""
        ids = [self.stores[i].id for i in range(10)]
        search = StoreSearch(ids=ids)
        stores = await self.repo.search_stores(search=search)

        self.assertEqual(stores.total, 10)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 1)
        self.assertEqual(len(stores.stores), 10)

        self.assertEqual(stores.next_page, None)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, False)
        self.assertEqual(stores.has_previous, False)

    async def test_search_stores_by_store_type(self) -> None:
        """Test the search stores by store type functionality."""
        await Store.objects.all().adelete()

        for _ in range(50):
            await self.acreate(store_type=1)

        for _ in range(50):
            await self.acreate(store_type=2)

        for _ in range(50):
            await self.acreate(store_type=3)

        search = StoreSearch(store_types=[1, 2])
        stores = await self.repo.search_stores(search=search)

        self.assertEqual(stores.total, 100)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 10)
        self.assertEqual(len(stores.stores), 10)

        self.assertEqual(stores.next_page, 2)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.has_previous, False)

        store_0 = stores.stores[0].model_dump()
        store_1 = stores.stores[1].model_dump()
        store_2 = stores.stores[2].model_dump()

        self.assertIn(store_0.get("store_type"), [1, 2])
        self.assertIn(store_1.get("store_type"), [1, 2])
        self.assertIn(store_2.get("store_type"), [1, 2])

    async def test_search_stores_by_created_on(self) -> None:
        """Test the search stores by created_on functionality."""
        await Store.objects.all().adelete()

        today = date.today()
        self.search.created_on = today
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)

    async def test_search_stores_by_created_before(self) -> None:
        """Test the search stores by created_before functionality."""
        await Store.objects.all().adelete()

        tomorrow = date.today() + timedelta(days=1)
        self.search.created_before = tomorrow
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)

    async def test_search_stores_by_created_after(self) -> None:
        """Test the search stores by created_after functionality."""
        await Store.objects.all().adelete()

        yesterday = date.today() - timedelta(days=1)
        self.search.created_after = yesterday
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)

    async def test_search_stores_by_updated_on(self) -> None:
        """Test the search stores by updated_on functionality."""
        await Store.objects.all().adelete()

        today = date.today()
        self.search.updated_on = today
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)

    async def test_search_stores_by_updated_before(self) -> None:
        """Test the search stores by updated_before functionality."""
        await Store.objects.all().adelete()

        tomorrow = date.today() + timedelta(days=1)
        self.search.updated_before = tomorrow
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)

    async def test_search_stores_by_updated_after(self) -> None:
        """Test the search stores by updated_after functionality."""
        await Store.objects.all().adelete()

        yesterday = date.today() - timedelta(days=1)
        self.search.updated_after = yesterday
        await self.acreate()

        stores = await self.repo.search_stores(search=self.search)
        self.assertEqual(stores.total, 1)
