"""Contains tests for the store router."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

MAPPING_ENDPOINT = "/api/v1/stores/types/mapping"


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
        return super().tearDown()

    def test_store_type_mapping(self) -> None:
        """Test getting store type mapping"""
        response = self.client.get(MAPPING_ENDPOINT)
        self.assertEqual(response.status_code, 200)

        response_json = response.json()
        self.assertEqual(response_json["1"], "Online")
        self.assertEqual(response_json["2"], "In-Store")
        self.assertEqual(response_json["3"], "Both")
