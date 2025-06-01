"""Test the store list functionality."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestStoreList(TestCase):
    """Test the store list functionality."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.stores = StoreFactory.create_batch(50)
        self.stores_for_user = StoreFactory.create_batch(50, user=self.user)
        self.repo = StoreRepo()

        self.acreate = sync_to_async(StoreFactory.create)

    async def test_get_stores(self) -> None:
        """Test the get stores functionality with no filters."""
        stores = await self.repo.get_stores()
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 10)

        self.assertEqual(stores.has_previous, False)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.next_page, 2)

    async def test_get_items_2nd_page(self) -> None:
        """Test the get stores functionality with no filters for page number 2."""
        stores = await self.repo.get_stores(page_number=2)
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 2)
        self.assertEqual(stores.total_pages, 10)

        self.assertEqual(stores.has_previous, True)
        self.assertEqual(stores.previous_page, 1)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.next_page, 3)

    async def test_get_stores_last_page(self) -> None:
        """Test the get stores functionality for page number 10."""
        stores = await self.repo.get_stores(page_number=10)
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 10)
        self.assertEqual(stores.total_pages, 10)

        self.assertEqual(stores.has_previous, True)
        self.assertEqual(stores.previous_page, 9)
        self.assertEqual(stores.has_next, False)
        self.assertEqual(stores.next_page, None)

    async def test_get_stores_page_after_last_page(self) -> None:
        """Test the get stores functionality for page number 12."""
        stores = await self.repo.get_stores(page_number=11)
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 10)
        self.assertEqual(stores.total_pages, 10)

        self.assertEqual(stores.has_previous, True)
        self.assertEqual(stores.previous_page, 9)
        self.assertEqual(stores.has_next, False)
        self.assertEqual(stores.next_page, None)

    async def test_get_stores_page_2_after_last_page(self) -> None:
        """Test the get stores functionality for page number 2 after the last page."""
        stores = await self.repo.get_stores(page_number=12)
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 10)
        self.assertEqual(stores.total_pages, 10)

        self.assertEqual(stores.has_previous, True)
        self.assertEqual(stores.previous_page, 9)
        self.assertEqual(stores.has_next, False)
        self.assertEqual(stores.next_page, None)

    async def test_get_stores_with_user(self) -> None:
        """Test the get stores functionality filtering by user."""
        stores = await self.repo.get_stores(user=self.user)
        self.assertEqual(stores.total, 50)
        self.assertEqual(len(stores.stores), 10)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 5)

        self.assertEqual(stores.has_previous, False)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.next_page, 2)

    async def test_get_stores_with_50_per_page(self) -> None:
        """Test the get stores functionality with 50 per page."""
        stores = await self.repo.get_stores(stores_per_page=50)
        self.assertEqual(stores.total, 100)
        self.assertEqual(len(stores.stores), 50)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 2)

        self.assertEqual(stores.has_previous, False)
        self.assertEqual(stores.previous_page, None)
        self.assertEqual(stores.has_next, True)
        self.assertEqual(stores.next_page, 2)

    async def test_get_stores_sorted_by_name(self) -> None:
        """Test the get stores functionality sorted by name."""
        await Store.objects.all().adelete()

        await self.acreate(name="A")
        await self.acreate(name="B")
        await self.acreate(name="C")

        stores = await self.repo.get_stores(sort="name")

        store_0 = stores.stores[0].model_dump()
        store_1 = stores.stores[1].model_dump()
        store_2 = stores.stores[2].model_dump()

        self.assertEqual(store_0.get("name"), "C")
        self.assertEqual(store_1.get("name"), "B")
        self.assertEqual(store_2.get("name"), "A")

    async def test_get_stores_sorted_by_name_asc(self) -> None:
        """Test the get stores functionality sorted by name in ascending order."""
        await Store.objects.all().adelete()

        await self.acreate(name="A")
        await self.acreate(name="B")
        await self.acreate(name="C")

        stores = await self.repo.get_stores(sort="name", sort_dir="asc")

        store_0 = stores.stores[0].model_dump()
        store_1 = stores.stores[1].model_dump()
        store_2 = stores.stores[2].model_dump()

        self.assertEqual(store_0.get("name"), "A")
        self.assertEqual(store_1.get("name"), "B")
        self.assertEqual(store_2.get("name"), "C")
