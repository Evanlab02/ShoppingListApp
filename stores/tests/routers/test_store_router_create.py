"""Contains tests for the store router."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = "Online"
TEST_DESCRIPTION = "Test description"
CREATE_ENDPOINT = "/api/v1/stores/create"
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
        self.client.force_login(self.user)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    def test_create_store(self) -> None:
        """Test creating a store."""
        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": TEST_STORE_TYPE,
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)

    def test_create_store_in_store_type(self) -> None:
        """Test creating a store with an in-store store type."""
        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": "In-Store",
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], "In-Store")
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)

    def test_create_store_both_store_type(self) -> None:
        """Test creating a store with a both store type."""
        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": "Both",
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], "Both")
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)

    def test_create_store_duplicate(self) -> None:
        """Test creating a store with a duplicate name."""
        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": TEST_STORE_TYPE,
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)

        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": TEST_STORE_TYPE,
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["detail"], f"Store '{TEST_STORE}' already exists."
        )

    def test_create_store_invalid_store_type(self) -> None:
        """Test creating a store with an invalid store type."""
        response = self.client.post(
            CREATE_ENDPOINT,
            {
                "name": TEST_STORE,
                "store_type": "Invalid",
                "description": TEST_DESCRIPTION,
            },
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Store type 'Invalid' is invalid.")
