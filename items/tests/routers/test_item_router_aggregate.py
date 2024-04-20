"""Contains tests for the item router aggregate function."""

from django.contrib.auth.models import User
from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestAggregationRouter(BaseTestCase):
    """Test the item router aggregation functions."""

    def setUp(self) -> None:
        """Set up the tests."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_aggregate_items(self) -> None:
        """Test that the items are aggregated."""
        response = self.client.get("/api/v1/items/aggregate")
        aggregation = response.json()
        self.assertEqual(aggregation["total_items"], 2)
        self.assertEqual(aggregation["total_price"], 300)
        self.assertEqual(aggregation["average_price"], 150)
        self.assertEqual(aggregation["max_price"], 200)
        self.assertEqual(aggregation["min_price"], 100)

    def test_aggregate_personal_items(self) -> None:
        """Test that the personal items are aggregated."""
        response = self.client.get("/api/v1/items/aggregate/me")
        aggregation = response.json()
        self.assertEqual(aggregation["total_items"], 2)
        self.assertEqual(aggregation["total_price"], 300)
        self.assertEqual(aggregation["average_price"], 150)
        self.assertEqual(aggregation["max_price"], 200)
        self.assertEqual(aggregation["min_price"], 100)

    def test_aggregate_personal_items_for_new_user(self) -> None:
        """Test that the personal items are aggregated for a new user."""
        user = User.objects.create(
            username="new_user",
            email="tester@gmail.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        user.save()

        self.client.logout()
        self.client.force_login(user)

        response = self.client.get("/api/v1/items/aggregate/me")
        aggregation = response.json()

        self.assertEqual(aggregation["total_items"], 0)
        self.assertEqual(aggregation["total_price"], None)
        self.assertEqual(aggregation["average_price"], None)
        self.assertEqual(aggregation["max_price"], None)
        self.assertEqual(aggregation["min_price"], None)
