"""Tests for the item delete view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class ItemDeleteViewTestCase(TestCase):
    """
    Tests for the item delete view.

    Tests: items.views.delete_page
    """

    def setUp(self) -> None:
        """
        Set up the test case.

        1. Create a test user.
        2. Create a test store.
        3. Create a test item.
        4. Create the test client.
        5. Login the test user.
        6. Create the URL for the item delete view.
        """
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(user=self.user, store=self.store)

        self.client = Client()
        self.client.force_login(self.user)

        self.url = reverse("item_delete_page", kwargs={"item_id": self.item.id})

    def test_item_delete_view_status_code_and_template(self) -> None:
        """
        Test the item delete view status code and template.

        Given: A user is logged in.
        When: The user visits the item delete view.
        Then: The response is 200.
        And: The template used is items/delete.html.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/delete.html")

    def test_item_delete_view_context(self) -> None:
        """
        Test the item delete view context.

        Given: A user is logged in.
        When: The user visits the item delete view.
        Then: The context is as expected.
        """
        response = self.client.get(self.url)
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

    def test_item_delete_view_requires_login(self) -> None:
        """
        Test the item delete view requires a login.

        Given: A user is logged out.
        When: The user visits the item delete view.
        Then: The response is 302.
        And: The user is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_delete_view_with_non_existent_item(self) -> None:
        """
        Test the item delete view with a non-existent item.

        Given: A user is logged in.
        When: The user visits the item delete view with a non-existent item id.
        Then: The response is 404.
        """
        response = self.client.get(reverse("item_delete_page", kwargs={"item_id": 999999}))
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/err/404.html")

    def test_item_delete_view_with_item_not_owned_by_user(self) -> None:
        """
        Test the item delete view with an item not owned by the user.

        Given: A user is logged in.
        When: The user visits the item delete view with an item not owned by the user.
        Then: The response is 404.
        """
        other_user = UserFactory.create()
        self.client.force_login(other_user)
        response = self.client.get(
            self.url,
        )
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/err/404.html")

    def test_item_delete_post(self) -> None:
        """
        Test the item delete view with a POST request.

        Given: A user is logged in.
        When: The user deletes the item using a POST request.
        Then: The response is 302.
        And: The user is redirected to the personalized overview page.
        And: The item is deleted.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('item_personalized_overview_page')}")
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())
