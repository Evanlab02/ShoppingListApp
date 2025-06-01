"""Contains tests for the store detail router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreDetailRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store detail router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.detail_url = reverse("ninja-api:store_get_detail", args=[self.store.id])

    def test_get_store_detail(self) -> None:
        """Test getting store details."""
        response = self.client.get(
            self.detail_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["id"], self.store.id)
        self.assertEqual(data["name"], self.store.name)
        self.assertEqual(data["store_type"], self.store.store_type)
        self.assertEqual(data["description"], self.store.description)

    def test_get_store_detail_not_found(self) -> None:
        """Test getting store details for non-existent store."""
        response = self.client.get(
            reverse("ninja-api:store_get_detail", args=[99999]),
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 404)

    def test_get_store_detail_no_token(self) -> None:
        """Test getting store details without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.detail_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_get_store_detail_other_user(self) -> None:
        """Test getting store details for another user's store."""
        other_user = UserFactory.create()
        other_store = StoreFactory.create(user=other_user)

        response = self.client.get(
            reverse("ninja-api:store_get_detail", args=[other_store.id]),
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()

        self.assertEqual(data["id"], other_store.id)
        self.assertEqual(data["name"], other_store.name)
        self.assertEqual(data["store_type"], other_store.store_type)
        self.assertEqual(data["description"], other_store.description)
