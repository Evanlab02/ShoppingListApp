"""Contains tests for the store list router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreListRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store list router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.list_url = reverse("ninja-api:store_get")
        self.personal_url = reverse("ninja-api:store_get_me")

    def test_get_stores_default_pagination(self) -> None:
        """Test getting stores with default pagination."""
        StoreFactory.create_batch(3, user=self.user)

        response = self.client.get(
            self.list_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 3)
        self.assertEqual(data["total"], 3)
        self.assertEqual(data["page_number"], 1)
        self.assertEqual(data["total_pages"], 1)
        self.assertFalse(data["has_previous"])
        self.assertIsNone(data["previous_page"])
        self.assertFalse(data["has_next"])
        self.assertIsNone(data["next_page"])

    def test_get_stores_custom_pagination(self) -> None:
        """Test getting stores with custom pagination."""
        StoreFactory.create_batch(15, user=self.user)

        response = self.client.get(
            f"{self.list_url}?limit=5&page=2",
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 5)
        self.assertEqual(data["total"], 15)
        self.assertEqual(data["page_number"], 2)
        self.assertEqual(data["total_pages"], 3)
        self.assertTrue(data["has_previous"])
        self.assertEqual(data["previous_page"], 1)
        self.assertTrue(data["has_next"])
        self.assertEqual(data["next_page"], 3)

    def test_get_stores_sorting(self) -> None:
        """Test getting stores with sorting."""
        StoreFactory.create(name="C Store", store_type=1, description="Test", user=self.user)
        StoreFactory.create(name="A Store", store_type=1, description="Test", user=self.user)
        StoreFactory.create(name="B Store", store_type=1, description="Test", user=self.user)

        response = self.client.get(
            f"{self.list_url}?sort=name&sort_dir=asc",
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["stores"][0]["name"], "A Store")
        self.assertEqual(data["stores"][1]["name"], "B Store")
        self.assertEqual(data["stores"][2]["name"], "C Store")

    def test_get_personal_stores(self) -> None:
        """Test getting personal stores."""
        StoreFactory.create_batch(2, user=self.user)

        other_user = UserFactory.create()
        StoreFactory.create(user=other_user)

        response = self.client.get(
            self.personal_url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 2)
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["page_number"], 1)
        self.assertEqual(data["total_pages"], 1)
        self.assertFalse(data["has_previous"])
        self.assertIsNone(data["previous_page"])
        self.assertFalse(data["has_next"])
        self.assertIsNone(data["next_page"])

    def test_get_stores_no_token(self) -> None:
        """Test getting stores without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.list_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_get_personal_stores_no_token(self) -> None:
        """Test getting personal stores without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.get(
            self.personal_url,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_get_stores_invalid_sort_field(self) -> None:
        """Test getting stores with invalid sort field."""
        response = self.client.get(
            f"{self.list_url}?sort=invalid_field",
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

    def test_get_stores_invalid_sort_direction(self) -> None:
        """Test getting stores with invalid sort direction."""
        response = self.client.get(
            f"{self.list_url}?sort=name&sort_dir=invalid",
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)
