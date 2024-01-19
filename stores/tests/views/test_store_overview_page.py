"""Test the store overview page."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

STORE_OVERVIEW_TEMPLATE = "stores/overview.html"


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
        self.store2 = Store.objects.create(
            name="Test Store 2",
            description="Test Description 2",
            store_type=3,
            user=self.user,
        )
        self.store2.save()
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
        self.assertTemplateUsed(response, STORE_OVERVIEW_TEMPLATE)

    def test_get_overview_page_not_logged_in(self) -> None:
        """Test the GET method for the overview page when not logged in."""
        self.client.logout()
        response = self.client.get("/stores/")
        self.assertTemplateNotUsed(response, STORE_OVERVIEW_TEMPLATE)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_get_overview_page_with_custom_page_number(self) -> None:
        """Test the GET method for the overview page with a custom page number."""
        response = self.client.get("/stores/?page=2&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, STORE_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        page_number = pagination.get("page_number")
        self.assertEqual(page_number, 2)

    def test_get_overview_page_with_custom_limit(self) -> None:
        """Test the GET method for the overview page with a custom limit."""
        response = self.client.get("/stores/?page=1&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, STORE_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        stores = pagination.get("stores")
        self.assertEqual(len(stores), 1)

    def test_get_overview_page_with_invalid_page_number(self) -> None:
        """Test the GET method for the overview page with an invalid page number."""
        response = self.client.get("/stores/?page=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, STORE_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        page_number = pagination.get("page_number")
        self.assertEqual(page_number, 1)

    def test_get_overview_page_with_invalid_limit(self) -> None:
        """Test the GET method for the overview page with an invalid limit."""
        response = self.client.get("/stores/?limit=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, STORE_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        stores = pagination.get("stores")
        self.assertEqual(len(stores), 2)
