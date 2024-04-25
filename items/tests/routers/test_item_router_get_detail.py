"""Contains tests for the item router detail function."""

from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestDetailRouter(BaseTestCase):
    """Test the item router detail functions."""

    def setUp(self) -> None:
        """Set up the tests."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def test_get_item_detail(self) -> None:
        """Test that the item detail is retrieved."""
        response = self.client.get(f"/api/v1/items/detail/{self.item.id}")
        item = response.json()
        self.assertEqual(item["name"], "Test Item")
        self.assertEqual(item["price"], "100.00")
        self.assertEqual(item["description"], "Test Description")

        self.assertEqual(item["store"]["name"], "Base Test Store")
        self.assertEqual(item["user"]["username"], self.user.username)

    def test_get_item_detail_not_found(self) -> None:
        """Test that the item detail is not found."""
        response = self.client.get("/api/v1/items/detail/100")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Item with id '100' does not exist."})
