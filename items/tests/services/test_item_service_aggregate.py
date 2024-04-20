"""Contains tests for the item service aggregate function."""

from django.contrib.auth.models import User

from items.services import item_service
from items.tests.base.base_test_case import BaseTestCase


class TestAggregationService(BaseTestCase):
    """Test the item service aggregation functions."""

    async def test_aggregate_items(self) -> None:
        """Test that the items are aggregated."""
        aggregation = await item_service.aggregate()
        self.assertEqual(aggregation.total_items, 2)
        self.assertEqual(aggregation.total_price, 300)
        self.assertEqual(aggregation.average_price, 150)
        self.assertEqual(aggregation.max_price, 200)
        self.assertEqual(aggregation.min_price, 100)

    async def test_aggregate_personal_items(self) -> None:
        """Test that the personal items are aggregated."""
        aggregation = await item_service.aggregate(user=self.user)
        self.assertEqual(aggregation.total_items, 2)
        self.assertEqual(aggregation.total_price, 300)
        self.assertEqual(aggregation.average_price, 150)
        self.assertEqual(aggregation.max_price, 200)
        self.assertEqual(aggregation.min_price, 100)

    async def test_aggregate_personal_items_for_new_user(self) -> None:
        """Test that the personal items are aggregated for a new user."""
        user = await User.objects.acreate(
            username="new_user",
            email="tester@gmail.com",
            password="password",
            first_name="Test",
            last_name="User",
        )
        await user.asave()

        aggregation = await item_service.aggregate(user=user)
        self.assertEqual(aggregation.total_items, 0)
        self.assertEqual(aggregation.total_price, None)
        self.assertEqual(aggregation.average_price, None)
        self.assertEqual(aggregation.max_price, None)
        self.assertEqual(aggregation.min_price, None)
