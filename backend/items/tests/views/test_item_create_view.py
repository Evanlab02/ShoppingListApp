"""Contains the tests for the item create view."""

from uuid import uuid4

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestItemCreateView(TestCase):
    """Test the item create view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.url = reverse("item_create_page")
        self.action_url = reverse("item_create_action")

        self.stores = StoreFactory.create_batch(20)

    def test_item_create_view_get(self) -> None:
        """Test the item create view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/create.html")

        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], "Create Item")
        self.assertEqual(context["is_personal"], False)
        self.assertEqual(context["is_overview"], False)
        self.assertEqual(context["show_advanced_navigation"], False)
        self.assertEqual(context["error"], None)

        # View Specific Context
        context_stores = context["stores"]
        self.assertEqual(len(context_stores), 20)

        ids_of_stores_in_context = [store["id"] for store in context_stores]
        ids_of_stores_in_db = [store.id for store in self.stores]

        ids_of_stores_in_context.sort()
        ids_of_stores_in_db.sort()

        self.assertEqual(ids_of_stores_in_context, ids_of_stores_in_db)

    def test_item_create_view_post(self) -> None:
        """Test the item create view with a POST should be forbidden."""
        response = self.client.post(self.url, data={"name": "Test Item"})
        self.assertEqual(response.status_code, 405)

    def test_item_create_view_needs_login(self) -> None:
        """Test the item create view needs a login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_item_create_action(self) -> None:
        """Test the item create action."""
        uuid = uuid4().hex
        data = {
            "item-input": f"Test Item {uuid}",
            "store-input": f"{self.stores[0].id}",
            "price-input": 100,
            "description-input": "Test Description",
        }

        response = self.client.post(self.action_url, data)
        self.assertEqual(response.status_code, 302)

        item = Item.objects.get(name=f"Test Item {uuid}")
        self.assertRedirects(response, reverse("item_detail_page", kwargs={"item_id": item.id}))

    def test_item_create_action_missing_fields(self) -> None:
        """Test the item create action with missing fields."""
        data = {
            "item-input": "Test Item",
            "store-input": f"{self.stores[0].id}",
            "price-input": "",
            "description-input": "",
        }
        response = self.client.post(self.action_url, data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.url}?error=Missing required fields.")

    def test_item_create_action_invalid_fields(self) -> None:
        """Test the item create action with invalid fields."""
        data = {
            "item-input": "Test Item",
            "store-input": f"{self.stores[0].id}",
            "price-input": "not a number",
            "description-input": "Test Description",
        }
        response = self.client.post(self.action_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.url}?error=Invalid input.")

    def test_item_create_action_item_already_exists(self) -> None:
        """Test the item create action with an item that already exists."""
        ItemFactory.create(name="Test Item", store=self.stores[0], user=self.user)
        data = {
            "item-input": "Test Item",
            "description-input": "Test Description",
            "price-input": 100,
            "store-input": f"{self.stores[0].id}",
        }
        response = self.client.post(self.action_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{self.url}?error=Item Already Exists.")

    def test_item_create_action_forbids_get_request(self) -> None:
        """Test the item create action forbids GET requests."""
        response = self.client.get(self.action_url)
        self.assertEqual(response.status_code, 405)

    def test_item_create_action_prevents_unauthorized_access(self) -> None:
        """Test the item create action prevents unauthorized access."""
        self.client.logout()
        response = self.client.post(self.action_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )
