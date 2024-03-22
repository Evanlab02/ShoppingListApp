"""Contains tests for the store router."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"
UPDATE_ENDPOINT = "/api/v1/stores/update"
CONTENT_TYPE = "application/json"


class TestStoreRouterUpdate(TestCase):
    """Test the store router update endpoint."""

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

    def test_store_update_no_params(self) -> None:
        """Test store update with no params."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/{self.store.id}",
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

    def test_store_update_name_param(self) -> None:
        """Test store update with name param."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/{self.store.id}?name=Tester",
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], "Tester")
        self.assertEqual(response_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)
        self.assertIsInstance(response_json["id"], int)
        self.assertIsNotNone(response_json.get("created_at"))
        self.assertIsNotNone(response_json.get("updated_at"))

    def test_store_update_type_param(self) -> None:
        """Test store update with store type param."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/{self.store.id}?store_type=3",
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], 3)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)
        self.assertIsInstance(response_json["id"], int)
        self.assertIsNotNone(response_json.get("created_at"))
        self.assertIsNotNone(response_json.get("updated_at"))

    def test_store_update_type_param_string_version(self) -> None:
        """Test store update with store type param."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/{self.store.id}?store_type=Both",
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], 3)
        self.assertEqual(response_json["description"], TEST_DESCRIPTION)
        self.assertIsInstance(response_json["id"], int)
        self.assertIsNotNone(response_json.get("created_at"))
        self.assertIsNotNone(response_json.get("updated_at"))

    def test_store_update_description(self) -> None:
        """Test store update with description."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/{self.store.id}",
            {"description": "New Test Description"},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["name"], TEST_STORE)
        self.assertEqual(response_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(response_json["description"], "New Test Description")
        self.assertIsInstance(response_json["id"], int)
        self.assertIsNotNone(response_json.get("created_at"))
        self.assertIsNotNone(response_json.get("updated_at"))

    def test_store_update_with_invalid_id(self) -> None:
        """Test store update with description."""
        response = self.client.put(
            f"{UPDATE_ENDPOINT}/9999",
            {"description": "Invalid Test ID..."},
            content_type=CONTENT_TYPE,
        )

        self.assertEqual(response.status_code, 404)

        response_json = response.json()
        self.assertEqual(response_json["detail"], "Store with id '9999' does not exist.")
