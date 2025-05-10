"""Contains tests for the get stores service."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.services.store_service import StoreService
from stores.tests.factory import StoreFactory


class TestGetStoresService(TestCase):
    """Tests for the get stores service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.store_service = StoreService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)

        self.bulk_create = sync_to_async(StoreFactory.create_batch)

    async def test_get_stores(self) -> None:
        """Test the get stores method."""
        stores = await self.store_service.get_stores(user=self.user)
        self.assertEqual(len(stores.stores), 1)

        store = stores.stores[0]
        store_dict = store.model_dump()
        self.assertEqual(store_dict.get("id"), self.store.id)
        self.assertEqual(store_dict.get("name"), self.store.name)
        self.assertEqual(store_dict.get("store_type"), self.store.store_type)
        self.assertEqual(store_dict.get("description"), self.store.description)
        self.assertIsNotNone(store_dict.get("created_at"))
        self.assertIsNotNone(store_dict.get("updated_at"))

        self.assertEqual(store_dict.get("user", {}).get("username"), self.user.username)

        self.assertEqual(stores.total, 1)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 1)
        self.assertFalse(stores.has_previous)
        self.assertFalse(stores.has_next)
        self.assertIsNone(stores.previous_page)
        self.assertIsNone(stores.next_page)

    async def test_get_stores_with_100_stores(self) -> None:
        """Test the get stores method with 100 stores."""
        await self.bulk_create(99, user=self.user)
        stores = await self.store_service.get_stores(user=self.user, page_number=1, limit=5)

        self.assertEqual(len(stores.stores), 5)
        self.assertEqual(stores.total, 100)
        self.assertEqual(stores.page_number, 1)
        self.assertEqual(stores.total_pages, 20)
        self.assertTrue(stores.has_next)
        self.assertEqual(stores.next_page, 2)
        self.assertFalse(stores.has_previous)
        self.assertIsNone(stores.previous_page)

        stores = await self.store_service.get_stores(user=self.user, page_number=2, limit=5)
        self.assertEqual(len(stores.stores), 5)
        self.assertEqual(stores.total, 100)
        self.assertEqual(stores.page_number, 2)
        self.assertEqual(stores.total_pages, 20)
        self.assertTrue(stores.has_previous)
        self.assertEqual(stores.previous_page, 1)
        self.assertTrue(stores.has_next)
        self.assertEqual(stores.next_page, 3)

        stores = await self.store_service.get_stores(user=self.user, page_number=20, limit=5)
        self.assertEqual(len(stores.stores), 5)
        self.assertEqual(stores.total, 100)
        self.assertEqual(stores.page_number, 20)
        self.assertEqual(stores.total_pages, 20)
        self.assertTrue(stores.has_previous)
        self.assertEqual(stores.previous_page, 19)
        self.assertFalse(stores.has_next)
        self.assertIsNone(stores.next_page)

    async def test_get_stores_with_sorting(self) -> None:
        """Test the get stores method with sorting."""
        await self.bulk_create(9, user=self.user)
        stores = await self.store_service.get_stores(user=self.user, sort="name", sort_dir="asc")

        # Verify stores are sorted by name in ascending order
        store_names = [store.model_dump().get("name") for store in stores.stores]
        self.assertEqual(store_names, sorted(store_names))

        stores = await self.store_service.get_stores(user=self.user, sort="name", sort_dir="desc")

        # Verify stores are sorted by name in descending order
        store_names = [store.model_dump().get("name") for store in stores.stores]
        self.assertEqual(store_names, sorted(store_names, reverse=True))
