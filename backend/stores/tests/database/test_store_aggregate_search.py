"""Contains tests for the aggregate with search function of the store repository."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.database.store_repo import StoreRepo
from stores.schemas.input import StoreSearch
from stores.tests.factory import StoreFactory


class TestStoreAggregateSearch(TestCase):
    """
    Test the aggregate with search function of the store repository.

    Tests: stores.database.store_repo.StoreRepo.aggregate_with_search
    """

    def setUp(self) -> None:
        """
        Set up the test.

        1. Create a user
        2. Create the store repo
        3. Create 3 stores for the user
        4. Create an async implementation for the user create method of the user factory
        """
        self.user = UserFactory.create()
        self.repo = StoreRepo()
        self.store_a = StoreFactory.create(
            name="Alpha",
            store_type=1,
            user=self.user,
        )
        StoreFactory.create(
            name="Beta",
            store_type=2,
            user=self.user,
        )
        StoreFactory.create(
            name="Charlie",
            store_type=3,
            user=self.user,
        )
        self.acreate_user = sync_to_async(UserFactory.create)
        return super().setUp()

    async def test_aggregate_stores_name(self) -> None:
        """
        Test the aggregate stores function when filtering by name.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the name "Alpha"
        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 0
        - Combined stores: 0
        - Total stores: 1
        """
        results = await self.repo.aggregate(name="Alpha")
        self.assertEqual(results["online_stores"], 1)
        self.assertEqual(results["in_store_stores"], 0)
        self.assertEqual(results["combined_stores"], 0)
        self.assertEqual(results["total_stores"], 1)

    async def test_aggregate_stores_user(self) -> None:
        """
        Test the aggregate stores function when filtering by user.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the user
        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 1
        - Combined stores: 1
        - Total stores: 3
        """
        results = await self.repo.aggregate(user=self.user)
        self.assertEqual(results["online_stores"], 1)
        self.assertEqual(results["in_store_stores"], 1)
        self.assertEqual(results["combined_stores"], 1)
        self.assertEqual(results["total_stores"], 3)

    async def test_aggregate_stores_alternate_user(self) -> None:
        """
        Test the aggregate stores function when filtering by alternate user.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the alternate user
        (that did not create the stores)

        Then: The aggregate function should return the following results:
        - Online stores: 0
        - In-store stores: 0
        - Combined stores: 0
        - Total stores: 0
        """
        alternate_user = await self.acreate_user()
        results = await self.repo.aggregate(user=alternate_user)
        self.assertEqual(results["online_stores"], 0)
        self.assertEqual(results["in_store_stores"], 0)
        self.assertEqual(results["combined_stores"], 0)
        self.assertEqual(results["total_stores"], 0)

    async def test_aggregate_stores_ids(self) -> None:
        """
        Test the aggregate stores function when filtering by id.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the id of the Alpha store

        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 0
        - Combined stores: 0
        - Total stores: 1
        """
        search = StoreSearch(ids=[self.store_a.id])
        results = await self.repo.aggregate(search=search)
        self.assertEqual(results["online_stores"], 1)
        self.assertEqual(results["in_store_stores"], 0)
        self.assertEqual(results["combined_stores"], 0)
        self.assertEqual(results["total_stores"], 1)

    async def test_aggregate_stores_type(self) -> None:
        """
        Test the aggregate stores function when filtering by store type.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the store types [1, 2]
        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 1
        - Combined stores: 0
        - Total stores: 2
        """
        search = StoreSearch(store_types=[1, 2])
        results = await self.repo.aggregate(search=search)
        self.assertEqual(results["online_stores"], 1)
        self.assertEqual(results["in_store_stores"], 1)
        self.assertEqual(results["combined_stores"], 0)
        self.assertEqual(results["total_stores"], 2)
