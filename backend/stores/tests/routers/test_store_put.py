"""Contains tests for the store put router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StorePutRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store put router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.put_url = reverse("ninja-api:store_put", args=[self.store.id])

    def test_put_store(self) -> None:
        """Test putting store with all fields."""
        new_name = "Updated Store Name"
        new_type = 2
        new_description = "Updated store description"

        response = self.client.put(
            self.put_url,
            {
                "name": new_name,
                "store_type": new_type,
                "description": new_description,
            },
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], new_name)
        self.assertEqual(data["store_type"], new_type)
        self.assertEqual(data["description"], new_description)

    def test_put_store_missing_fields(self) -> None:
        """Test putting store with missing fields."""
        response = self.client.put(
            self.put_url,
            {
                "name": "New Name",
                "store_type": 1,
            },
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)

    def test_put_store_not_found(self) -> None:
        """Test putting non-existent store."""
        response = self.client.put(
            reverse("ninja-api:store_put", args=[99999]),
            {
                "name": "New Name",
                "store_type": 1,
                "description": "New description",
            },
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_put_store_no_token(self) -> None:
        """Test putting store without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.put(
            self.put_url,
            {
                "name": "New Name",
                "store_type": 1,
                "description": "New description",
            },
            headers=self.base_headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_put_store_other_user(self) -> None:
        """Test putting another user's store."""
        other_user = UserFactory.create()
        other_store = StoreFactory.create(user=other_user)

        response = self.client.put(
            reverse("ninja-api:store_put", args=[other_store.id]),
            {
                "name": "New Name",
                "store_type": 1,
                "description": "New description",
            },
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
