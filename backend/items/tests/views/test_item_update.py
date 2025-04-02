"""Contains the tests for the item update view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestItemUpdateView(TestCase):
    """Test the item update view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)

        self.stores = StoreFactory.create_batch(20)
        self.item = ItemFactory.create(user=self.user, store=self.stores[0])
        self.url = reverse("item_update_page", kwargs={"item_id": self.item.id})
        self.action_url = reverse("item_update_action")

    def test_item_update_view_get(self) -> None:
        """Test the item update view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/update.html")

        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], "Update Item")
        self.assertFalse(context["is_personal"])
        self.assertFalse(context["is_overview"])
        self.assertFalse(context["show_advanced_navigation"])

        # Item Context
        self.assertEqual(context["item"]["id"], self.item.id)
        self.assertEqual(context["item"]["name"], self.item.name)
        self.assertEqual(context["item"]["description"], self.item.description)
        self.assertEqual(context["item"]["price"], self.item.price)

        # Stores Context
        self.assertEqual(len(context["stores"]), 20)

    def test_item_update_view_post(self) -> None:
        """Test the item update view with a POST request."""
        response = self.client.post(self.url, data={"name": "Test Item"})
        self.assertEqual(response.status_code, 405)

    def test_item_update_view_needs_login(self) -> None:
        """Test the item update view needs a login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_update_with_invalid_item_id(self) -> None:
        """Test the item update view with an invalid item id."""
        url = reverse("item_update_page", kwargs={"item_id": 999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_item_update_action(self) -> None:
        """Test the item update action."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": self.item.id,
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('item_detail_page', kwargs={'item_id': self.item.id})}",
        )

        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.store, self.stores[1])
        self.assertEqual(self.item.price, 999888)
        self.assertEqual(self.item.description, "Test Description")

    def test_item_update_action_invalid_method(self) -> None:
        """Test the item update action with an invalid method."""
        response = self.client.get(self.action_url)
        self.assertEqual(response.status_code, 405)

    def test_item_update_action_when_not_logged_in(self) -> None:
        """Test the item update action when not logged in."""
        self.client.logout()
        response = self.client.post(self.action_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_update_action_invalid_id(self) -> None:
        """Test the item update action with an invalid id."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": "not an int",
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Could not format input for item update, please try again.", response.content
        )

    def test_item_update_action_invalid_store_id(self) -> None:
        """Test the item update action with an invalid store id."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": self.item.id,
                "item-input": "Test Item",
                "store-input": "not an int",
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Could not format input for item update, please try again.", response.content
        )

    def test_item_update_action_invalid_price(self) -> None:
        """Test the item update action with an invalid price."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": self.item.id,
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": "not a number",
                "description-input": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(
            b"Could not format input for item update, please try again.", response.content
        )

    def test_item_update_action_empty_id(self) -> None:
        """Test the item update action with an empty id."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": "",
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Could not find ID for update, please try again.", response.content)

    def test_item_update_action_with_non_existent_item(self) -> None:
        """Test the item update action with a non-existent item."""
        response = self.client.post(
            self.action_url,
            data={
                "item-id": 999999,
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Could not find item with ID: 999999.", response.content)

    def test_item_update_action_with_item_already_exists(self) -> None:
        """Test the item update action with an item that already exists."""
        item = ItemFactory.create(user=self.user, store=self.stores[1], name="Test Item")
        response = self.client.post(
            self.action_url,
            data={
                "item-id": item.id,
                "item-input": "Test Item",
                "store-input": self.stores[1].id,
                "price-input": 999888,
                "description-input": "Test Description",
            },
        )
        expected_error = "Item already exists in that store."
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('item_update_page', kwargs={'item_id': item.id})}?error={expected_error}",
        )
