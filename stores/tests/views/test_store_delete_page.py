"""Test the store delete view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE_NAME = "Test Store"


class TestStoreDeleteView(TestCase):
    """Test the store delete view."""

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
            name=TEST_STORE_NAME,
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

    def test_get_delete_page(self) -> None:
        """Test get delete page."""
        response = self.client.get(f"/stores/delete/{self.store.id}")
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 200)
        self.assertEqual(content, b"Attempted to access delete page.")
