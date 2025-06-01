"""Contains tests for the delete_store function of the store repository."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestStoreDelete(TestCase):
    """Test the delete_store function of the store repository."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = StoreRepo()

    async def test_delete_store(self) -> None:
        """Test the delete_store function of the store repository."""
        await self.repo.delete_store(self.store.id, self.user)
        exists = await Store.objects.filter(id=self.store.id).aexists()
        self.assertFalse(exists)

    async def test_delete_store_does_not_exist(self) -> None:
        """Test the delete_store function of the store repository when the store does not exist."""
        with self.assertRaises(Store.DoesNotExist):
            await self.repo.delete_store(99999999999, self.user)
