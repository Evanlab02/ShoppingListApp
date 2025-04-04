"""Contains tests for the aggregate function of the store repository."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.tests.factory import StoreFactory


class TestStoreAggregate(TestCase):
    """Test the aggregate function of the store repository."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.stores = StoreFactory.create_batch(3, user=self.user)
        self.repo = StoreRepo()
        return super().setUp()

    async def test_aggregate_stores(self) -> None:
        """Test the aggregate stores function."""
        expected_online_stores = len([store for store in self.stores if store.store_type == 1])
        expected_in_store_stores = len([store for store in self.stores if store.store_type == 2])
        expected_combined_stores = len([store for store in self.stores if store.store_type == 3])
        expected_total_stores = len(self.stores)

        # Create a store with a different user
        results = await self.repo.aggregate(user=self.user)
        self.assertEqual(results["online_stores"], expected_online_stores)
        self.assertEqual(results["in_store_stores"], expected_in_store_stores)
        self.assertEqual(results["combined_stores"], expected_combined_stores)
        self.assertEqual(results["total_stores"], expected_total_stores)
