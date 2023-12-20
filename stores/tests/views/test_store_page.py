"""Contains tests for the store create view."""
import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.views import CREATE_PAGE


class TestStoreCreateView(TestCase):
    """Test the store create view."""

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
        self.client.force_login(self.user)

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_create_page(self) -> None:
        """Test the create page."""
        response = self.client.get(f"/stores/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/create.html")

    def test_get_create_page_not_logged_in(self) -> None:
        """Test the create page when not logged in."""
        self.client.logout()
        response = self.client.get(f"/stores/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/?next=/stores/create", 302, 200)
