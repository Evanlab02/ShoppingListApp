"""Test the store update functionality."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestStoreUpdate(TestCase):
    """Test the store update functionality."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = StoreRepo()

    async def test_item_update_name(self) -> None:
        """Test the item update name functionality."""
        store = await self.repo.update_store(
            store_id=self.store.id,
            user=self.user,
            store_name="New Name",
            store_type=None,
            store_description=None,
        )
        self.assertEqual(store.name, "New Name")
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(await store.auser(), self.user)

    async def test_item_update_type(self) -> None:
        """Test the item update type functionality."""
        store = await self.repo.update_store(
            store_id=self.store.id,
            user=self.user,
            store_name=None,
            store_type=3,
            store_description=None,
        )
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(await store.auser(), self.user)

    async def test_item_update_description(self) -> None:
        """Test the item update description functionality."""
        store = await self.repo.update_store(
            store_id=self.store.id,
            user=self.user,
            store_name=None,
            store_type=None,
            store_description="New Description",
        )
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, "New Description")
        self.assertEqual(await store.auser(), self.user)

    async def test_item_update_all(self) -> None:
        """Test the item update all functionality."""
        store = await self.repo.update_store(
            store_id=self.store.id,
            user=self.user,
            store_name="New Name",
            store_type=3,
            store_description="New Description",
        )
        self.assertEqual(store.name, "New Name")
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, "New Description")
        self.assertEqual(await store.auser(), self.user)

    async def test_item_update_does_not_exist(self) -> None:
        """Test the item update does not exist functionality."""
        with self.assertRaises(Store.DoesNotExist):
            await self.repo.update_store(
                store_id=99999999999,
                user=self.user,
                store_name=None,
                store_type=None,
                store_description=None,
            )
