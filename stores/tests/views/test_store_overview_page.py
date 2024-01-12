"""Test the store overview page."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store


class TestStoreOverviewPage(TestCase):
    """Test the store overview page."""

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

    def test_get_overview_page(self) -> None:
        """Test the GET method for the overview page."""
        response = self.client.get("/stores/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/overview.html")

    def test_get_overview_page_not_logged_in(self) -> None:
        """Test the GET method for the overview page when not logged in."""
        self.client.logout()
        response = self.client.get("/stores/")
        self.assertTemplateNotUsed(response, "stores/overview.html")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )
