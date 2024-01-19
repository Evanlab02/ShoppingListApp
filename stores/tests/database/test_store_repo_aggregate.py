"""Test the aggregate function of the store repository."""

from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import aggregate_stores
from stores.models import ShoppingStore as Store


class TestStoreRepoAggregate(TestCase):
    """Test the aggregate function of the store repository."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()

        for store_number in range(1, 6):
            store = Store.objects.create(
                name=f"Test Store {store_number}",
                store_type=store_number % 3 + 1,
                user=self.user,
            )
            store.save()

        return super().setUp()

    async def test_aggregate(self) -> None:
        """Test the aggregate function."""
        result = await aggregate_stores()
        self.assertIsInstance(result, dict)

        self.assertEqual(result["total_stores"], 5)
        self.assertEqual(result["online_stores"], 1)
        self.assertEqual(result["in_store_stores"], 2)
        self.assertEqual(result["combined_stores"], 2)

    async def test_aggregate_by_user(self) -> None:
        """Test the aggregate function."""
        result = await aggregate_stores(user=self.user)
        self.assertIsInstance(result, dict)

        self.assertEqual(result["total_stores"], 5)
        self.assertEqual(result["online_stores"], 1)
        self.assertEqual(result["in_store_stores"], 2)
        self.assertEqual(result["combined_stores"], 2)

    async def test_aggregate_by_user_no_stores(self) -> None:
        """Test the aggregate function."""
        user = await User.objects.acreate(
            username="testuser2",
            email="testuser2@gmail.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        await user.asave()

        result = await aggregate_stores(user=user)
        self.assertIsInstance(result, dict)

        self.assertEqual(result["total_stores"], 0)
        self.assertEqual(result["online_stores"], 0)
        self.assertEqual(result["in_store_stores"], 0)
        self.assertEqual(result["combined_stores"], 0)
