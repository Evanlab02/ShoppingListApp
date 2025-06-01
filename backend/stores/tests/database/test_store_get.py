"""Test the store get."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestStoreGet(TestCase):
    """Test the store get."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = StoreRepo()

    async def test_get_store(self) -> None:
        """Test the get store."""
        store = await self.repo.get_store(self.store.id)
        self.assertEqual(store.id, self.store.id)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.created_at, self.store.created_at)
        self.assertEqual(store.updated_at, self.store.updated_at)

    async def test_get_store_does_not_exist(self) -> None:
        """Test the get store does not exist."""
        with self.assertRaises(Store.DoesNotExist):
            await self.repo.get_store(99999999999)
