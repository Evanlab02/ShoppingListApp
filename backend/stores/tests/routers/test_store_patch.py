"""Contains tests for the store patch router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StorePatchRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store patch router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.store = StoreFactory.create(user=self.user)
        self.patch_url = reverse("ninja-api:store_patch", args=[self.store.id])

    def test_patch_store_name(self) -> None:
        """Test patching store name."""
        new_name = "Updated Store Name"
        response = self.client.patch(
            self.patch_url,
            {"name": new_name},
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], new_name)
        self.assertEqual(data["store_type"], self.store.store_type)
        self.assertEqual(data["description"], self.store.description)

    def test_patch_store_type(self) -> None:
        """Test patching store type."""
        new_type = 2
        response = self.client.patch(
            self.patch_url,
            {"store_type": new_type},
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.store.name)
        self.assertEqual(data["store_type"], new_type)
        self.assertEqual(data["description"], self.store.description)

    def test_patch_store_description(self) -> None:
        """Test patching store description."""
        new_description = "Updated store description"
        response = self.client.patch(
            self.patch_url,
            {"description": new_description},
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.store.name)
        self.assertEqual(data["store_type"], self.store.store_type)
        self.assertEqual(data["description"], new_description)

    def test_patch_store_multiple_fields(self) -> None:
        """Test patching multiple store fields."""
        new_name = "Updated Store Name"
        new_type = 2
        new_description = "Updated store description"

        response = self.client.patch(
            self.patch_url,
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

    def test_patch_store_not_found(self) -> None:
        """Test patching non-existent store."""
        response = self.client.patch(
            reverse("ninja-api:store_patch", args=[99999]),
            {"name": "New Name"},
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)

    def test_patch_store_no_token(self) -> None:
        """Test patching store without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.patch(
            self.patch_url,
            {"name": "New Name"},
            headers=self.base_headers,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 401)

    def test_patch_store_other_user(self) -> None:
        """Test patching another user's store."""
        other_user = UserFactory.create()
        other_store = StoreFactory.create(user=other_user)

        response = self.client.patch(
            reverse("ninja-api:store_patch", args=[other_store.id]),
            {"name": "New Name"},
            headers=self.base_headers,
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 404)
