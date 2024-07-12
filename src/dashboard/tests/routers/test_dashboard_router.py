"""Contains tests for the dashboard router."""

from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestDeleteEndpoint(BaseTestCase):
    """Test the delete endpoint in the item router."""

    def setUp(self) -> None:
        """Set up the tests."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the tests."""
        return super().tearDown()

    def test_session_overview_api(self) -> None:
        """Test the overview API."""
        response = self.client.get("/api/v1/dashboard/session/overview")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(response_body["total"], 0)
        self.assertEqual(response_body["total_price"], 0)
        self.assertEqual(response_body["budget_remaining"], 0)
        self.assertEqual(response_body["average_item_price"], 0)

    def test_session_recent_items_api(self) -> None:
        """Test the recent items API."""
        response = self.client.get("/api/v1/dashboard/session/recent/items")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(response_body["items"], [])

    def test_session_history_api(self) -> None:
        """Test the history API."""
        response = self.client.get("/api/v1/dashboard/session/history")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(
            response_body["labels"],
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
            ],
        )
        self.assertEqual(
            response_body["data"],
            [
                {
                    "label": "Price",
                    "data": [65, 59, 80, 81, 56, 55],
                },
                {
                    "label": "Budget",
                    "data": [28, 48, 40, 19, 86, 27],
                },
            ],
        )

    def test_token_overview_api(self) -> None:
        """Test the overview API."""
        response = self.client.get("/api/v1/dashboard/token/overview")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(response_body["total"], 0)
        self.assertEqual(response_body["total_price"], 0)
        self.assertEqual(response_body["budget_remaining"], 0)
        self.assertEqual(response_body["average_item_price"], 0)

    def test_token_recent_items_api(self) -> None:
        """Test the recent items API."""
        response = self.client.get("/api/v1/dashboard/token/recent/items")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(response_body["items"], [])

    def test_token_history_api(self) -> None:
        """Test the history API."""
        response = self.client.get("/api/v1/dashboard/token/history")
        self.assertEqual(response.status_code, 200)

        response_body = response.json()
        self.assertEqual(
            response_body["labels"],
            [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
            ],
        )
        self.assertEqual(
            response_body["data"],
            [
                {
                    "label": "Price",
                    "data": [65, 59, 80, 81, 56, 55],
                },
                {
                    "label": "Budget",
                    "data": [28, 48, 40, 19, 86, 27],
                },
            ],
        )
