"""Test the store update view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store


class TestStoreUpdateView(TestCase):
    """Test the store update view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="user@test.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()
        self.store = Store.objects.create(
            name="Test Store",
            description="Test Description",
            store_type=3,
            user=self.user,
        )
        self.store.save()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_update_page(self) -> None:
        """Test the update page."""
        response = self.client.get("/stores/update/1")
        self.assertEqual(
            response.content,
            b"WIP: Attempted to retrieve page to update store ID: 1.",
        )
