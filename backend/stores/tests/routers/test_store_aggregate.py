"""Contains tests for the store aggregate router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreAggregateRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store aggregate router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.aggregate_url = reverse("ninja-api:store_aggregate")
        self.aggregate_me_url = reverse("ninja-api:store_aggregate_me")

    def test_get_store_aggregation(self) -> None:
        """Test getting store aggregation for all stores."""
        # Create stores with different types
        StoreFactory.create_batch(3, store_type=1, user=self.user)  # Online stores
        StoreFactory.create_batch(2, store_type=2, user=self.user)  # Physical stores
        StoreFactory.create(store_type=3, user=self.user)  # Combined store

        # Create stores for another user
        other_user = UserFactory.create()
        StoreFactory.create_batch(2, store_type=1, user=other_user)
        StoreFactory.create(store_type=2, user=other_user)

        response = self.client.get(
            self.aggregate_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Test aggregation fields that are actually calculated
        self.assertEqual(data["total_stores"], 9)
        self.assertEqual(data["online_stores"], 5)  # Online stores
        self.assertEqual(data["in_store_stores"], 3)  # Physical stores
        self.assertEqual(data["combined_stores"], 1)  # Combined stores

    def test_get_store_aggregation_by_user(self) -> None:
        """Test getting store aggregation for user's own stores."""
        # Create stores for the test user
        StoreFactory.create_batch(3, store_type=1, user=self.user)  # Online stores
        StoreFactory.create_batch(2, store_type=2, user=self.user)  # Physical stores
        StoreFactory.create(store_type=3, user=self.user)  # Combined store

        # Create stores for another user
        other_user = UserFactory.create()
        StoreFactory.create_batch(2, store_type=1, user=other_user)
        StoreFactory.create(store_type=2, user=other_user)

        response = self.client.get(
            self.aggregate_me_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Test aggregation fields that are actually calculated (should only include user's stores)
        self.assertEqual(data["total_stores"], 6)
        self.assertEqual(data["online_stores"], 3)  # Online stores
        self.assertEqual(data["in_store_stores"], 2)  # Physical stores
        self.assertEqual(data["combined_stores"], 1)  # Combined stores

    def test_get_store_aggregation_no_stores(self) -> None:
        """Test getting store aggregation when there are no stores."""
        response = self.client.get(
            self.aggregate_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Test aggregation fields that are actually calculated
        self.assertEqual(data["total_stores"], 0)
        self.assertEqual(data["online_stores"], 0)
        self.assertEqual(data["in_store_stores"], 0)
        self.assertEqual(data["combined_stores"], 0)

    def test_get_store_aggregation_by_user_no_stores(self) -> None:
        """Test getting store aggregation when user has no stores."""
        response = self.client.get(
            self.aggregate_me_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Test aggregation fields that are actually calculated
        self.assertEqual(data["total_stores"], 0)
        self.assertEqual(data["online_stores"], 0)
        self.assertEqual(data["in_store_stores"], 0)
        self.assertEqual(data["combined_stores"], 0)

    def test_get_store_aggregation_no_token(self) -> None:
        """Test getting store aggregation without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.aggregate_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_get_store_aggregation_by_user_no_token(self) -> None:
        """Test getting store aggregation by user without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.aggregate_me_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)
