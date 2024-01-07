"""Contains tests for the aggregation endpoint of the stores app."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"


class TestAggregation(TestCase):
    """Contains tests for the aggregation endpoint."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testing123",
        )
        self.user.save()
        self.store = Store.objects.create(
            name=TEST_STORE,
            store_type=TEST_STORE_TYPE,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()
        self.alt_user = User.objects.create_user(
            username="altuser",
            email="altuser@gmail.com",
            password="testing123",
        )
        self.alt_user.save()
        self.alt_store = Store.objects.create(
            name="Alt Store",
            store_type=3,
            description="Alt Description",
            user=self.alt_user,
        )
        self.alt_store.save()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    def test_aggregation(self) -> None:
        """Test the aggregation endpoint."""
        result = self.client.get("/api/v1/stores/aggregate")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total_stores"], 2)
        self.assertEqual(result_json["online_stores"], 1)
        self.assertEqual(result_json["in_store_stores"], 0)
        self.assertEqual(result_json["combined_stores"], 1)
        self.assertEqual(result_json["combined_online_stores"], 2)
        self.assertEqual(result_json["combined_in_store_stores"], 1)

    def test_aggregation_by_user(self) -> None:
        """Test the aggregation endpoint by user."""
        self.client.force_login(self.user)
        result = self.client.get("/api/v1/stores/aggregate/me")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total_stores"], 1)
        self.assertEqual(result_json["online_stores"], 1)
        self.assertEqual(result_json["in_store_stores"], 0)
        self.assertEqual(result_json["combined_stores"], 0)
        self.assertEqual(result_json["combined_online_stores"], 1)
        self.assertEqual(result_json["combined_in_store_stores"], 0)
