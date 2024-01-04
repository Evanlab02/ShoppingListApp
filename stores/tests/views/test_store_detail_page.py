"""Contains tests for the store detail view."""
import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEMPLATE = "stores/detail.html"


class TestStoreDetailView(TestCase):
    """Test the store detail view."""

    @pytest.mark.django_db(transaction=True)
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

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_detail_page(self) -> None:
        """Test the GET method for the detail page."""
        response = self.client.get(f"/stores/detail/{self.store.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, TEMPLATE)

    def test_get_detail_page_unauthorized(self) -> None:
        """Test the GET method for the detail page."""
        self.client.logout()
        response = self.client.get(f"/stores/detail/{self.store.id}")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, TEMPLATE)

    def test_get_detail_page_invalid_id(self) -> None:
        """Test the GET method for the detail page."""
        response = self.client.get("/stores/detail/4000")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateNotUsed(response, TEMPLATE)
        self.assertEqual(response.content, b"This store does not exist.")
