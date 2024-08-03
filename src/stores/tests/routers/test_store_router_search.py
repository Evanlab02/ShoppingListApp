"""Contains tests for the search endpoint of the stores app."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"
CONTENT_TYPE = "application/json"


class TestSearch(TestCase):
    """Contains tests for the search endpoint."""

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

    def test_search_by_name(self) -> None:
        """Test the search endpoint by name."""
        result = self.client.post("/api/v1/stores/search?name=Store", {}, content_type=CONTENT_TYPE)
        self.assertEqual(result.status_code, 200)
        result_json = result.json()
        self.assertEqual(result_json["total"], 2)
        self.assertEqual(len(result_json["stores"]), 2)

        result = self.client.post(
            "/api/v1/stores/search?name=Alt Store", {}, content_type=CONTENT_TYPE
        )
        result_json = result.json()
        self.assertEqual(result_json["total"], 1)
        self.assertEqual(len(result_json["stores"]), 1)

    def test_search_for_own(self) -> None:
        """Test searching for owned items."""
        self.client.force_login(self.user)
        result = self.client.post("/api/v1/stores/search?own=true", {}, content_type=CONTENT_TYPE)
        result_json = result.json()
        self.assertEqual(result_json["total"], 1)
        self.assertEqual(len(result_json["stores"]), 1)
