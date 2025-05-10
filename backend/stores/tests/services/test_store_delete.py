"""Contains tests for the delete method of the store service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.errors.exceptions import StoreDoesNotExist
from stores.services.store_service import StoreService
from stores.tests.factory import StoreFactory


class TestStoreDelete(TestCase):
    """Test the delete method of the store service."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.service = StoreService()

    async def test_delete_store(self) -> None:
        """Test the delete method of the store service."""
        await self.service.delete(self.store.id, self.user)
        with self.assertRaises(StoreDoesNotExist):
            await self.service.get_store(self.store.id)

    async def test_delete_store_does_not_exist(self) -> None:
        """Test the delete method of the store service when the store does not exist."""
        with self.assertRaises(StoreDoesNotExist):
            await self.service.delete(99999999999, self.user)
