"""Contains tests for the item update view."""

from django.test import Client

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
