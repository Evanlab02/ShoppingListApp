"""Test the store service get."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.errors.exceptions import StoreDoesNotExist
from stores.services.store_service import StoreService
from stores.tests.factory import StoreFactory


class TestStoreServiceGet(TestCase):
    """Test the store service get."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.service = StoreService()

    async def test_get_store(self) -> None:
        """Test the get store."""
        store = await self.service.get_store(self.store.id)
        self.assertEqual(store.id, self.store.id)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.created_at, self.store.created_at)
        self.assertEqual(store.updated_at, self.store.updated_at)

    async def test_get_store_does_not_exist(self) -> None:
        """Test the get store does not exist."""
        with self.assertRaises(StoreDoesNotExist):
            await self.service.get_store(99999999999)
