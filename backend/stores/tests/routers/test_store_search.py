"""Contains tests for the store search router."""

from django.urls import reverse

from authentication.tests.factory import UserFactory
from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.tests.factory import StoreFactory


class StoreSearchRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store search router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.search_url = reverse("ninja-api:store_search")

    def test_search_stores_by_name(self) -> None:
        """Test searching stores by name."""
        StoreFactory.create(name="Test Store 1", store_type=1, user=self.user)
        StoreFactory.create(name="Other Store", store_type=1, user=self.user)
        StoreFactory.create(name="Test Store 2", store_type=1, user=self.user)

        response = self.client.post(
            self.search_url,
            {"name": "Test"},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 2)
        self.assertEqual(data["total"], 2)
        self.assertTrue(all("Test" in store["name"] for store in data["stores"]))

    def test_search_stores_by_store_type(self) -> None:
        """Test searching stores by store type."""
        StoreFactory.create(name="Online Store", store_type=1, user=self.user)
        StoreFactory.create(name="Physical Store", store_type=2, user=self.user)
        StoreFactory.create(name="Combined Store", store_type=3, user=self.user)

        response = self.client.post(
            self.search_url,
            {
                "store_types": [1, 2],
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 2)
        self.assertEqual(data["total"], 2)
        self.assertTrue(all(store["store_type"] in [1, 2] for store in data["stores"]))

    def test_search_stores_by_ids(self) -> None:
        """Test searching stores by IDs."""
        store1 = StoreFactory.create(name="Store 1", store_type=1, user=self.user)
        StoreFactory.create(name="Store 2", store_type=1, user=self.user)
        store3 = StoreFactory.create(name="Store 3", store_type=1, user=self.user)

        response = self.client.post(
            self.search_url,
            {
                "ids": [store1.id, store3.id],
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 2)
        self.assertEqual(data["total"], 2)
        self.assertTrue(all(store["id"] in [store1.id, store3.id] for store in data["stores"]))

    def test_search_stores_with_pagination(self) -> None:
        """Test searching stores with pagination."""
        StoreFactory.create_batch(15, user=self.user)

        response = self.client.post(
            f"{self.search_url}?page=2&limit=5",
            {},
            content_type=self.content_type,
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

    def test_search_stores_with_sorting(self) -> None:
        """Test searching stores with sorting."""
        StoreFactory.create(name="C Store", store_type=1, user=self.user)
        StoreFactory.create(name="A Store", store_type=1, user=self.user)
        StoreFactory.create(name="B Store", store_type=1, user=self.user)

        response = self.client.post(
            f"{self.search_url}?sort=name&sort_dir=asc",
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["stores"][0]["name"], "A Store")
        self.assertEqual(data["stores"][1]["name"], "B Store")
        self.assertEqual(data["stores"][2]["name"], "C Store")

    def test_search_own_stores(self) -> None:
        """Test searching only own stores."""
        StoreFactory.create_batch(2, user=self.user)
        other_user = UserFactory.create()
        StoreFactory.create(user=other_user)

        response = self.client.post(
            self.search_url,
            {"own": True},
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 2)
        self.assertEqual(data["total"], 2)

    def test_search_stores_no_token(self) -> None:
        """Test searching stores without authentication."""
        self.base_headers.pop("X-API-Token")
        response = self.client.post(
            self.search_url,
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 401)

    def test_search_stores_invalid_sort_field(self) -> None:
        """Test searching stores with invalid sort field."""
        response = self.client.post(
            f"{self.search_url}?sort=invalid_field",
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

    def test_search_stores_invalid_sort_direction(self) -> None:
        """Test searching stores with invalid sort direction."""
        response = self.client.post(
            f"{self.search_url}?sort=name&sort_dir=invalid",
            {},
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

    def test_search_stores_combined_filters(self) -> None:
        """Test searching stores with combined filters."""
        store1 = StoreFactory.create(name="Test Store 1", store_type=1, user=self.user)
        StoreFactory.create(name="Test Store 2", store_type=2, user=self.user)
        StoreFactory.create(name="Other Store", store_type=1, user=self.user)

        response = self.client.post(
            self.search_url,
            {
                "name": "Test",
                "store_types": [1],
                "ids": [store1.id],
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["stores"]), 1)
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["stores"][0]["id"], store1.id)
