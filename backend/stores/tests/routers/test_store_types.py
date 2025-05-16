"""Contains tests for the store types router."""

from django.urls import reverse

from shoppingapp.tests.base_router_test_case import BaseRouterTestCase


class StoreTypesRouterTestCase(BaseRouterTestCase):
    """Contains tests for the store types router."""

    def setUp(self) -> None:
        """Set up the test case."""
        super().setUp()
        self.url = reverse("ninja-api:store_types_mapping")

    def test_get_store_types_mapping(self) -> None:
        """Test the store types mapping endpoint."""
        response = self.client.get(
            self.url,
            headers=self.base_headers,
        )

        self.assertEqual(response.status_code, 200)

        # Test response data
        response_json = response.json()
        self.assertEqual(
            response_json,
            {
                "1": "Online",
                "2": "In-Store",
                "3": "Both",
            },
        )
        self.assertEqual(len(response_json), 3)
        self.assertEqual(response_json["1"], "Online")
        self.assertEqual(response_json["2"], "In-Store")
        self.assertEqual(response_json["3"], "Both")

    def test_get_store_types_mapping_without_auth(self) -> None:
        """Test the store types mapping endpoint without authentication."""
        response = self.client.get(
            self.url,
        )

        self.assertEqual(response.status_code, 401)
