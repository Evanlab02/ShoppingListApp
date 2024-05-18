"""Contains API tests for the delete item endpoint."""

from items.tests.api.base_test_case import BaseTestCase


class TestItemDeleteEndpoint(BaseTestCase):
    """Tests for the delete item endpoint."""

    def test_delete_endpoint(self) -> None:
        """Test that a user can delete an item."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/delete/{self.item.id}"
        response = self.session.delete(url)

        status_code = response.status_code
        self.assertEqual(status_code, 200)

        response_body = response.json()
        message = response_body["message"]
        detail = response_body["detail"]

        self.assertEqual(message, "Deleted Item.")
        self.assertEqual(detail, f"Item with ID #{self.item.id} was deleted.")

    def test_delete_endpoint_for_item_that_does_not_exist(self) -> None:
        """Test that a user cannot delete an item that does not exist."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/delete/9999999"
        response = self.session.delete(url)

        status_code = response.status_code
        self.assertEqual(status_code, 404)

        response_body = response.json()
        detail = response_body["detail"]
        self.assertEqual(detail, "Item with id '9999999' does not exist.")

    def test_delete_endpoint_invalid_method(self) -> None:
        """Test that the delete endpoint only allows DELETE requests."""
        self._login()
        url = f"{self.live_server_url}/api/v1/items/delete/{self.item.id}"
        response = self.session.get(url)

        status_code = response.status_code
        self.assertEqual(status_code, 405)
