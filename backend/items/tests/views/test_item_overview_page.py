"""Test the item overview page."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

ITEM_OVERVIEW_TEMPLATE = "items/overview.html"
MOCK_ITEM_NAME = "Crumbed Chicken"


class TestItemOverviewPage(TestCase):
    """Test the item overview page."""

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

        self.item = Item.objects.create(
            name=MOCK_ITEM_NAME,
            description="",
            price=100,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        self.item2 = Item.objects.create(
            name="Logitech headphones",
            description="",
            price=2500,
            store=self.store2,
            user=self.user,
        )
        self.item2.save()

        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Store.objects.all().delete()
        Item.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_overview_page(self) -> None:
        """Test the GET method for the overview page."""
        response = self.client.get("/items/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

    def test_get_personalized_overview_page(self) -> None:
        """Test the GET method for the personalized overview page."""
        response = self.client.get("/items/me")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

    def test_get_overview_page_not_logged_in(self) -> None:
        """Test the GET method for the overview page when not logged in."""
        self.client.logout()
        response = self.client.get("/items/")
        self.assertTemplateNotUsed(response, ITEM_OVERVIEW_TEMPLATE)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_get_personalized_overview_page_not_logged_in(self) -> None:
        """Test the GET method for the personalized overview page when not logged in."""
        self.client.logout()
        response = self.client.get("/items/me")
        self.assertTemplateNotUsed(response, ITEM_OVERVIEW_TEMPLATE)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_get_overview_page_with_custom_page_number(self) -> None:
        """Test the GET method for the overview page with a custom page number."""
        response = self.client.get("/items/?page=2&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        page_number = pagination.get("page_number")
        self.assertEqual(page_number, 2)

    def test_get_personalized_overview_page_with_custom_page_number(self) -> None:
        """Test the GET method for the personalized overview page with a custom page number."""
        response = self.client.get("/items/me?page=2&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        page_number = pagination.get("page_number")
        self.assertEqual(page_number, 2)

    def test_get_overview_page_with_custom_limit(self) -> None:
        """Test the GET method for the overview page with a custom limit."""
        response = self.client.get("/items/?page=1&limit=1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        items = pagination.get("items")
        self.assertEqual(len(items), 1)

    def test_get_overview_page_with_invalid_page_number(self) -> None:
        """Test the GET method for the overview page with an invalid page number."""
        response = self.client.get("/items/?page=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        page_number = pagination.get("page_number")
        self.assertEqual(page_number, 1)

    def test_get_overview_page_with_invalid_limit(self) -> None:
        """Test the GET method for the overview page with an invalid limit."""
        response = self.client.get("/items/?limit=invalid")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, ITEM_OVERVIEW_TEMPLATE)

        pagination = response.context.get("pagination", {})
        items = pagination.get("items")
        self.assertEqual(len(items), 2)
