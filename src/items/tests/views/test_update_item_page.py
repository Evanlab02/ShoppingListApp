"""Contains tests for the item update view."""

from asgiref.sync import async_to_sync
from django.test import Client

from items.models import ShoppingItem as Item
from items.tests.base.base_test_case import BaseTestCase


class TestItemUpdateView(BaseTestCase):
    """Contain tests for the item update view."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test."""
        self.client.logout()
        return super().tearDown()

    def test_update_action_view_with_badly_formatted_id(self) -> None:
        """Test the update action view with a badly formatted item id."""
        response = self.client.post(
            "/items/update/action",
            {
                "item-id": "badly-formatted-id",
                "item-input": "Some item",
                "store-input": "1",
                "price-input": "10.00",
                "description-input": "Some description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Invalid input.", 302, 404)

    def test_update_action_view_with_badly_formatted_store_id(self) -> None:
        """Test the update action view with a badly formatted store id."""
        response = self.client.post(
            "/items/update/action",
            {
                "item-id": "1",
                "item-input": "Some item",
                "store-input": "badly-formatted-id",
                "price-input": "10.00",
                "description-input": "Some description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Invalid input.", 302, 404)

    def test_update_action_view_with_badly_formatted_price(self) -> None:
        """Test the update action view with a badly formatted price."""
        response = self.client.post(
            "/items/update/action",
            {
                "item-id": "1",
                "item-input": "Some item",
                "store-input": "1",
                "price-input": "badly-formatted-price",
                "description-input": "Some description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Invalid input.", 302, 404)

    def test_update_action_view_with_no_item_id(self) -> None:
        """Test the update action view with no item id."""
        response = self.client.post(
            "/items/update/action",
            {
                "item-input": "Some item",
                "store-input": "1",
                "price-input": "10.00",
                "description-input": "Some description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Item ID is required.", 302, 404)

    def test_update_action_on_item_that_does_not_exist(self) -> None:
        """Test updating an item that does not exist."""
        response = self.client.post(
            "/items/update/action",
            {
                "item-id": "99999",
                "item-input": "Some item",
                "store-input": "1",
                "price-input": "10.00",
                "description-input": "Some description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Item does not exist.", 302, 404)

    def test_update_action_duplicate_item(self) -> None:
        """Test updating an item that already exists."""
        store = async_to_sync(self.create_temporary_store)()
        item = async_to_sync(self.create_temporary_item)(store=store)

        response = self.client.post(
            "/items/update/action",
            {
                "item-id": item.id,
                "item-input": item.name,
                "store-input": store.id,
                "price-input": item.price,
                "description-input": item.description,
            },
        )
        self.assertRedirects(response, "/items/update?error=Item already exists.", 302, 404)

    def test_update_action_view(self) -> None:
        """Test the update action view."""
        store = async_to_sync(self.create_temporary_store)()

        response = self.client.post(
            "/items/update/action",
            {
                "item-id": self.item.id,
                "item-input": "Updated item",
                "store-input": store.id,
                "price-input": 20.00,
                "description-input": "Updated description",
            },
        )
        self.assertRedirects(response, f"/items/detail/{self.item.id}", 302, 200)

        updated_item = Item.objects.get(id=self.item.id)
        self.assertEqual(updated_item.name, "Updated item")
        self.assertEqual(updated_item.store.id, store.id)
        self.assertEqual(updated_item.price, 20.00)
        self.assertEqual(updated_item.description, "Updated description")

    def test_update_action_invalid_method(self) -> None:
        """Test the update action view with an invalid method."""
        response = self.client.get("/items/update/action")
        self.assertEqual(response.status_code, 405)

    def test_update_action_does_not_work_when_not_logged_in(self) -> None:
        """Test the update action view when the user is not logged in."""
        self.client.logout()

        response = self.client.post(
            "/items/update/action",
            {
                "item-id": self.item.id,
                "item-input": "Updated item",
                "store-input": 1,
                "price-input": 20.00,
                "description-input": "Updated description",
            },
        )
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_update_action_does_not_let_you_update_other_users_items(self) -> None:
        """Test the update action view when trying to update another user's item."""
        user = async_to_sync(self.create_temporary_user)()
        self.client.logout()
        self.client.force_login(user)

        response = self.client.post(
            "/items/update/action",
            {
                "item-id": self.item.id,
                "item-input": "Updated item",
                "store-input": 1,
                "price-input": 20.00,
                "description-input": "Updated description",
            },
        )
        self.assertRedirects(response, "/items/update?error=Item does not exist.", 302, 404)
