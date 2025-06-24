"""Contains tests for the aggregate with search function of the store service."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.schemas.input import StoreSearch
from stores.services.store_service import StoreService
from stores.tests.factory import StoreFactory


class TestStoreServiceAggregateSearch(TestCase):
    """
    Test the aggregate with search function of the store service.

    Tests: stores.services.store_service.StoreService.aggregate
    """

    def setUp(self) -> None:
        """
        Set up the test.

        1. Create a user
        2. Create 3 stores for the user
        3. Create the store service
        4. Create an async implementation for the user create method of the user factory
        """
        self.user = UserFactory.create()
        self.store_a = StoreFactory.create(
            name="Alpha",
            store_type=1,
            user=self.user,
        )
        self.store_b = StoreFactory.create(
            name="Beta",
            store_type=2,
            user=self.user,
        )
        self.store_c = StoreFactory.create(
            name="Charlie",
            store_type=3,
            user=self.user,
        )
        self.service = StoreService()
        self.acreate_user = sync_to_async(UserFactory.create)
        return super().setUp()

    async def test_aggregate_by_user(self) -> None:
        """
        Test the aggregate function when filtering by user.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the user

        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 1
        - Combined stores: 1
        - Combined online stores: 2
        - Combined in-store stores: 2
        - Total stores: 3
        """
        results = await self.service.aggregate(user=self.user)
        self.assertEqual(results.online_stores, 1)
        self.assertEqual(results.in_store_stores, 1)
        self.assertEqual(results.combined_stores, 1)
        self.assertEqual(results.combined_online_stores, 2)
        self.assertEqual(results.combined_in_store_stores, 2)
        self.assertEqual(results.total_stores, 3)

    async def test_aggregate_by_alternate_user(self) -> None:
        """
        Test the aggregate function when filtering by alternate user.

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
        - Combined online stores: 0
        - Combined in-store stores: 0
        - Total stores: 0
        """
        alternate_user = await self.acreate_user()
        results = await self.service.aggregate(user=alternate_user)
        self.assertEqual(results.online_stores, 0)
        self.assertEqual(results.in_store_stores, 0)
        self.assertEqual(results.combined_stores, 0)
        self.assertEqual(results.combined_online_stores, 0)
        self.assertEqual(results.combined_in_store_stores, 0)
        self.assertEqual(results.total_stores, 0)

    async def test_aggregate_by_name(self) -> None:
        """
        Test the aggregate function when filtering by name.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the name "Alpha"

        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 0
        - Combined stores: 0
        - Combined online stores: 1
        - Combined in-store stores: 0
        - Total stores: 1
        """
        results = await self.service.aggregate(name="Alpha")
        self.assertEqual(results.online_stores, 1)
        self.assertEqual(results.in_store_stores, 0)
        self.assertEqual(results.combined_stores, 0)
        self.assertEqual(results.combined_online_stores, 1)
        self.assertEqual(results.combined_in_store_stores, 0)
        self.assertEqual(results.total_stores, 1)

    async def test_aggregate_by_ids(self) -> None:
        """
        Test the aggregate function when filtering by ids.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the ids of the Alpha and Charlie stores

        Then: The aggregate function should return the following results:
        - Online stores: 1
        - In-store stores: 0
        - Combined stores: 1
        - Combined online stores: 2
        - Combined in-store stores: 1
        - Total stores: 2
        """
        search = StoreSearch(ids=[self.store_a.id, self.store_c.id])
        results = await self.service.aggregate(search=search)
        self.assertEqual(results.online_stores, 1)
        self.assertEqual(results.in_store_stores, 0)
        self.assertEqual(results.combined_stores, 1)
        self.assertEqual(results.combined_online_stores, 2)
        self.assertEqual(results.combined_in_store_stores, 1)
        self.assertEqual(results.total_stores, 2)

    async def test_aggregate_by_store_types(self) -> None:
        """
        Test the aggregate function when filtering by store types.

        Given: Three stores are created with the following details:
        - Alpha: Online store
        - Beta: In-store store
        - Charlie: Combined store

        When: The aggregate function is called with the store types [2, 3] (in-store and combined)

        Then: The aggregate function should return the following results:
        - Online stores: 0
        - In-store stores: 1
        - Combined stores: 1
        - Combined online stores: 0
        - Combined in-store stores: 2
        - Total stores: 2
        """
        search = StoreSearch(store_types=[2, 3])
        results = await self.service.aggregate(search=search)
        self.assertEqual(results.online_stores, 0)
        self.assertEqual(results.in_store_stores, 1)
        self.assertEqual(results.combined_stores, 1)
        self.assertEqual(results.combined_online_stores, 1)
        self.assertEqual(results.combined_in_store_stores, 2)
        self.assertEqual(results.total_stores, 2)
