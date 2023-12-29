"""Contains tests for the store router."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"
DETAIL_ENDPOINT = "/api/v1/stores/detail"
CONTENT_TYPE = "application/json"


class TestStoreRouter(TestCase):
    """Test the store router."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.user.save()
        self.store = Store.objects.create(
            name=TEST_STORE,
            store_type=TEST_STORE_TYPE,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()
        self.client.force_login(self.user)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    def test_get_store_detail(self) -> None:
        """Test getting a store detail."""
        response = self.client.get(
            f"{DETAIL_ENDPOINT}/{self.store.id}",
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)
        self.assertIsInstance(response_json["id"], int)
        self.assertIsNotNone(response_json.get("created_at"))
        self.assertIsNotNone(response_json.get("updated_at"))
