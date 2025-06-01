"""Contains tests for the store create router."""

from django.urls import reverse

from shoppingapp.tests.base_router_test_case import BaseRouterTestCase
from stores.models import ShoppingStore as Store


class StoreCreateRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store create router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.url = reverse("ninja-api:store_create")

    def test_create_store(self) -> None:
        """Test the create store endpoint."""
        response = self.client.post(
            self.url,
            {
                "name": "Test Store",
                "store_type": 1,  # Online
                "description": "A test store",
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        # Test status code
        self.assertEqual(response.status_code, 201)

        # Test response data
        response_json = response.json()
        actual_name = response_json["name"]
        actual_store_type = response_json["store_type"]
        actual_description = response_json["description"]

        self.assertEqual(actual_name, "Test Store")
        self.assertEqual(actual_store_type, 1)
        self.assertEqual(actual_description, "A test store")

        # Test DB content
        store = Store.objects.get(id=response_json["id"])
        self.assertEqual(store.name, "Test Store")
        self.assertEqual(store.store_type, 1)
        self.assertEqual(store.description, "A test store")
        self.assertEqual(store.user, self.user)

    def test_create_store_with_no_token(self) -> None:
        """Test the create store endpoint with no token."""
        self.base_headers.pop("X-API-Token")
        response = self.client.post(
            self.url,
            {
                "name": "Test Store",
                "store_type": 1,
                "description": "A test store",
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        # Test status code
        self.assertEqual(response.status_code, 401)

    def test_create_store_missing_required_fields(self) -> None:
        """Test the create store endpoint with missing required fields."""
        # Test missing name
        response = self.client.post(
            self.url,
            {
                "store_type": 1,
                "description": "A test store",
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

        # Test missing store_type
        response = self.client.post(
            self.url,
            {
                "name": "Test Store",
                "description": "A test store",
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

        # Test missing description
        response = self.client.post(
            self.url,
            {
                "name": "Test Store",
                "store_type": 1,
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )
        self.assertEqual(response.status_code, 422)

    def test_create_store_invalid_store_type(self) -> None:
        """Test the create store endpoint with invalid store type."""
        response = self.client.post(
            self.url,
            {
                "name": "Test Store",
                "store_type": 999,  # Invalid store type
                "description": "A test store",
            },
            content_type=self.content_type,
            headers=self.base_headers,
        )

        # Test status code
        self.assertEqual(response.status_code, 400)
