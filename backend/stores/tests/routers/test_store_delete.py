"""Contains tests for the store delete router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreDeleteRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store delete router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.delete_url = reverse("ninja-api:store_delete", args=[self.store.id])

    def test_delete_store(self) -> None:
        """Test deleting store."""
        response = self.client.delete(
            self.delete_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Store deleted successfully")
        self.assertEqual(data["detail"], f"Store with id #{self.store.id} has been deleted.")

    def test_delete_store_not_found(self) -> None:
        """Test deleting non-existent store."""
        response = self.client.delete(
            reverse("ninja-api:store_delete", args=[99999]),
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 404)

    def test_delete_store_no_token(self) -> None:
        """Test deleting store without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.delete(
            self.delete_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_store_other_user(self) -> None:
        """Test deleting another user's store."""
        other_user = UserFactory.create()
        other_store = StoreFactory.create(user=other_user)

        response = self.client.delete(
            reverse("ninja-api:store_delete", args=[other_store.id]),
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 404)
