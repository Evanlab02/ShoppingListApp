"""Contains tests for the create_store function of the store repository."""

from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo


class TestStoreCreate(TestCase):
    """Test the create_store function of the store repository."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.repo = StoreRepo()
        return super().setUp()

    async def test_create_store(self) -> None:
        """Test the create_store function of the store repository."""
        store = await self.repo.create_store(
            name="Test Store",
            store_type=1,
            description="Test Description",
            user=self.user,
        )

        self.assertEqual(store.name, "Test Store")
        self.assertEqual(store.store_type, 1)
        self.assertEqual(store.description, "Test Description")
        self.assertEqual(store.user, self.user)
