"""Contains tests for the store aggregate search router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreAggregateSearchRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store aggregate search router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.aggregate_search_url = reverse("ninja-api:store_aggregate_search")

    # Helper -----------------------------------------------------------------

    def _assert_aggregation(
        self,
        data: dict[str, int],
        *,
        total: int,
        online: int,
        in_store: int,
        combined: int,
    ) -> None:
        """Assert that the aggregation matches expected values."""
        self.assertEqual(data["total_stores"], total)
        self.assertEqual(data["online_stores"], online)
        self.assertEqual(data["in_store_stores"], in_store)
        self.assertEqual(data["combined_stores"], combined)

    # Tests ------------------------------------------------------------------

    def test_get_store_aggregation_search_all(self) -> None:
        """Test getting aggregated stats without any filters (all stores)."""
        # Create stores for the authenticated user
        StoreFactory.create_batch(3, store_type=1, user=self.user)  # Online
        StoreFactory.create_batch(2, store_type=2, user=self.user)  # Physical
        StoreFactory.create(store_type=3, user=self.user)  # Combined

        # Create stores for another user
        other_user = UserFactory.create()
        StoreFactory.create_batch(2, store_type=1, user=other_user)
        StoreFactory.create(store_type=2, user=other_user)

        response = self.client.post(
            self.aggregate_search_url,
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_aggregation(data, total=9, online=5, in_store=3, combined=1)

    def test_get_store_aggregation_search_by_own(self) -> None:
        """Test aggregation when filtering by the authenticated user's stores only."""
        # Stores for test user
        StoreFactory.create_batch(4, store_type=1, user=self.user)
        StoreFactory.create_batch(3, store_type=2, user=self.user)
        StoreFactory.create_batch(2, store_type=3, user=self.user)

        # Stores for another user (should be ignored)
        other_user = UserFactory.create()
        StoreFactory.create_batch(5, store_type=1, user=other_user)
        StoreFactory.create_batch(2, store_type=2, user=other_user)

        response = self.client.post(
            self.aggregate_search_url,
            {"own": True},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_aggregation(data, total=9, online=4, in_store=3, combined=2)

    def test_get_store_aggregation_search_by_ids(self) -> None:
        """Test aggregation when filtering by specific store IDs."""
        # Create several stores and collect some IDs
        selected_stores = [
            StoreFactory.create(store_type=1),
            StoreFactory.create(store_type=2),
            StoreFactory.create(store_type=3),
        ]
        # Additional stores that should be ignored
        StoreFactory.create_batch(5)

        selected_ids = [store.id for store in selected_stores[:2]]  # Only first two IDs

        response = self.client.post(
            self.aggregate_search_url,
            {"ids": selected_ids},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_aggregation(data, total=2, online=1, in_store=1, combined=0)

    def test_get_store_aggregation_search_by_store_types(self) -> None:
        """Test aggregation when filtering by store types."""
        # Create various store types
        StoreFactory.create_batch(6, store_type=1)
        StoreFactory.create_batch(4, store_type=2)
        StoreFactory.create_batch(3, store_type=3)

        response = self.client.post(
            self.aggregate_search_url,
            {"store_types": [1, 2]},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_aggregation(data, total=10, online=6, in_store=4, combined=0)

    def test_get_store_aggregation_search_by_name(self) -> None:
        """Test aggregation when filtering by name substring."""
        # Create stores with specific naming
        StoreFactory.create(name="Alpha Mart", store_type=1)
        StoreFactory.create(name="Beta Shop", store_type=2)
        StoreFactory.create(name="Gamma Plaza", store_type=3)
        # Other unrelated stores
        StoreFactory.create_batch(5)

        response = self.client.post(
            self.aggregate_search_url,
            {"name": "Alpha"},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self._assert_aggregation(data, total=1, online=1, in_store=0, combined=0)

    def test_get_store_aggregation_search_no_token(self) -> None:
        """Test accessing the endpoint without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.post(
            self.aggregate_search_url,
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
