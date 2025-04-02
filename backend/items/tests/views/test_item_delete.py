"""Tests for the item delete view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemDeleteViewTestCase(TestCase):
    """Tests for the item delete view."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(user=self.user, store=self.store)

        self.client = Client()
        self.client.force_login(self.user)

    def test_item_delete_view(self) -> None:
        """Test the item delete view."""
        response = self.client.get(reverse("item_delete_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/delete.html")

        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], "Delete Item")
        self.assertFalse(context["is_personal"])
        self.assertFalse(context["is_overview"])
        self.assertFalse(context["show_advanced_navigation"])

        # Item Context
        self.assertEqual(context["item"]["id"], self.item.id)
        self.assertEqual(context["item"]["name"], self.item.name)
        self.assertEqual(context["item"]["description"], self.item.description)
        self.assertEqual(context["item"]["price"], self.item.price)
        self.assertEqual(context["item"]["created_at"], self.item.created_at)
        self.assertEqual(context["item"]["updated_at"], self.item.updated_at)
        self.assertEqual(context["item"]["user"]["username"], self.user.username)
        self.assertEqual(context["item"]["store"]["id"], self.item.store.id)

    def test_item_delete_view_requires_get_request(self) -> None:
        """Test the item delete view requires a GET request."""
        response = self.client.post(reverse("item_delete_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 405)

    def test_item_delete_view_requires_login(self) -> None:
        """Test the item delete view requires a login."""
        self.client.logout()
        response = self.client.get(reverse("item_delete_page", kwargs={"item_id": self.item.id}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_delete_view_with_non_existent_item(self) -> None:
        """Test the item delete view with a non-existent item."""
        response = self.client.get(reverse("item_delete_page", kwargs={"item_id": 999999}))
        self.assertEqual(response.status_code, 404)

    def test_item_delete_view_with_item_not_owned_by_user(self) -> None:
        """Test the item delete view with an item not owned by the user."""
        other_user = UserFactory.create()
        self.client.force_login(other_user)
        response = self.client.get(
            reverse("item_delete_page", kwargs={"item_id": self.item.id}),
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Item does not exist.", response.content)

    def test_item_delete_action(self) -> None:
        """Test the item delete action."""
        response = self.client.post(
            reverse("item_delete_action"),
            data={"item-id": self.item.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('item_personalized_overview_page')}")

    def test_item_delete_action_requires_post_request(self) -> None:
        """Test the item delete action requires a POST request."""
        response = self.client.get(reverse("item_delete_action"))
        self.assertEqual(response.status_code, 405)

    def test_item_delete_action_requires_login(self) -> None:
        """Test the item delete action requires a login."""
        self.client.logout()
        response = self.client.post(reverse("item_delete_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_delete_action_invalid_id(self) -> None:
        """Test the item delete action with an invalid id."""
        response = self.client.post(
            reverse("item_delete_action"),
            data={"item-id": "not an int"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Could not format input for item deletion, please try again.", response.content
        )

    def test_item_delete_action_empty_id(self) -> None:
        """Test the item delete action with an empty id."""
        response = self.client.post(
            reverse("item_delete_action"),
            data={"item-id": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Could not find ID for deletion, please try again.", response.content)

    def test_item_delete_action_with_non_existent_item(self) -> None:
        """Test the item delete action with a non-existent item."""
        response = self.client.post(
            reverse("item_delete_action"),
            data={"item-id": 999999},
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Could not find item with ID: 999999.", response.content)
