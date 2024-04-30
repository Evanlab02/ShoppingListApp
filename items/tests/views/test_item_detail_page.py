"""Contains tests for the item detail view."""

from django.test import Client

from items.tests.base.base_test_case import BaseTestCase


class TestItemDetailView(BaseTestCase):
    """Contain tests for the item detail view."""

    def setUp(self) -> None:
        """Set up the test."""
        super().setUp()
        self.client = Client()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test."""
        self.client.logout()
        return super().tearDown()

    def test_detail_view_incorrect_method(self) -> None:
        """Test that requesting the detail view with a post method returns status code: '405'."""
        response = self.client.post(f"/items/detail/{self.item.id}")
        status_code = response.status_code
        self.assertEqual(405, status_code)

    def test_detail_view_not_logged_in(self) -> None:
        """Test that requesting the detail view when not logged in returns status code: '302'."""
        self.client.logout()
        response = self.client.get(f"/items/detail/{self.item.id}")
        status_code = response.status_code
        self.assertEqual(302, status_code)

    def test_detail_view_returns_correct_status_code(self) -> None:
        """Test that requesting the detail view returns status code: '200'."""
        response = self.client.get(f"/items/detail/{self.item.id}")
        status_code = response.status_code
        self.assertEqual(200, status_code)

    def test_detail_view_with_item_that_does_not_exist_returns_404(self) -> None:
        """Test that requesting the detail view returns status code: '404'."""
        response = self.client.get("/items/detail/999999")
        status_code = response.status_code
        content = response.content
        self.assertEqual(404, status_code)
        self.assertEqual(content, b"Item with id '999999' does not exist.")
