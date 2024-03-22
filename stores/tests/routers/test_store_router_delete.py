"""Contains tests for the store router."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"
DELETE_ENDPOINT = "/api/v1/stores/delete"
CONTENT_TYPE = "application/json"


class TestStoreRouterDelete(TestCase):
    """Test the store router delete endpoint."""

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
        self.alt_user = User.objects.create_user(
            username="altuser",
            email="altuser@gmail.com",
            password="testing123",
        )
        self.alt_user.save()
        self.client.force_login(self.user)
        return super().setUp()

    def test_delete_store_success(self) -> None:
        """Test that delete is sucessful."""
        result = self.client.delete(f"{DELETE_ENDPOINT}/{self.store.id}")
        status_code = result.status_code
        self.assertEqual(status_code, 200)

        response_body = result.json()
        message = response_body.get("message")
        self.assertEqual(message, "Deleted Store.")

        detail = response_body.get("detail")
        self.assertEqual(detail, f"Store with ID #{self.store.id} was deleted.")

    def test_delete_store_invalid_id(self) -> None:
        """Test that delete fails when the ID provided does not exist."""
        result = self.client.delete(f"{DELETE_ENDPOINT}/99999")
        status_code = result.status_code
        self.assertEqual(status_code, 404)

        response_body = result.json()

        detail = response_body.get("detail")
        self.assertEqual(detail, "Store with id '99999' does not exist.")

    def test_delete_store_invalid_user(self) -> None:
        """Test that delete fails when a user that does not own the store, tries to delete it."""
        self.client.logout()
        self.client.force_login(self.alt_user)

        result = self.client.delete(f"{DELETE_ENDPOINT}/{self.store.id}")

        status_code = result.status_code
        self.assertEqual(status_code, 404)

        response_body = result.json()

        detail = response_body.get("detail")
        self.assertEqual(detail, f"Store with id '{self.store.id}' does not exist.")
