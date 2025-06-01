"""Contains tests for the does_store_exist function of the store repository."""

from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.tests.factory import StoreFactory


class TestDoesStoreExist(TestCase):
    """Test the does_store_exist function of the store repository."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.repo = StoreRepo()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        return super().setUp()

    async def test_store_exists(self) -> None:
        """Test that the store exists."""
        self.assertTrue(await self.repo.does_store_exist(self.store.id))

    async def test_store_does_not_exist(self) -> None:
        """Test that the store does not exist."""
        self.assertFalse(await self.repo.does_store_exist(99999999))
