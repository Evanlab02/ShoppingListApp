"""Contains tests for the item detail view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory


class TestItemDetailView(TestCase):
    """Tests for the item detail view."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = Client()
        self.user = UserFactory.create()
        self.item = ItemFactory.create(user=self.user)
        self.client.force_login(self.user)

    def test_item_detail_view(self) -> None:
        """Test the item detail view."""
        response = self.client.get(reverse("item_detail_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/detail.html")

        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], f"Item - {self.item.name}")
        self.assertFalse(context["is_personal"])
        self.assertFalse(context["is_overview"])
        self.assertTrue(context["show_advanced_navigation"])

        # Item Context
        self.assertEqual(context["item"]["id"], self.item.id)
        self.assertEqual(context["item"]["name"], self.item.name)
        self.assertEqual(context["item"]["description"], self.item.description)
        self.assertEqual(context["item"]["price"], self.item.price)
        self.assertEqual(context["item"]["created_at"], self.item.created_at)
        self.assertEqual(context["item"]["updated_at"], self.item.updated_at)
        self.assertEqual(context["item"]["user"]["username"], self.user.username)
        self.assertEqual(context["item"]["store"]["id"], self.item.store.id)

    def test_item_detail_view_requires_get_request(self) -> None:
        """Test the item detail view requires a GET request."""
        response = self.client.post(reverse("item_detail_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 405)

    def test_item_detail_view_requires_login(self) -> None:
        """Test the item detail view requires a login."""
        self.client.logout()
        response = self.client.get(reverse("item_detail_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )
