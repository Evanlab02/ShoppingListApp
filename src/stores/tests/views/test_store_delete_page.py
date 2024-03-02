"""Test the store delete view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE_NAME = "Test Store"
DELETE_ACTION = "/stores/delete/action"


class TestStoreDeleteView(TestCase):
    """Test the store delete view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="user@test.com",
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()
        self.store = Store.objects.create(
            name=TEST_STORE_NAME,
            description="Test Description",
            store_type=3,
            user=self.user,
        )
        self.store.save()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_delete_page(self) -> None:
        """Test get delete page."""
        response = self.client.get(f"/stores/delete/{self.store.id}")
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/delete.html")

    def test_delete_action(self) -> None:
        """Test the delete action."""
        response = self.client.post(DELETE_ACTION, {"store_id": f"{self.store.id}"})
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(response, "/stores/me", 302, 200)

    def test_delete_action_no_store_id(self) -> None:
        """Test the delete action with no store id."""
        response = self.client.post(DELETE_ACTION)
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 500)
        self.assertEqual(
            content, b"Unexpected Error: Request Failed due to store id not being provided."
        )

    def test_delete_action_invalid_store_id(self) -> None:
        """Test the delete action with invalid store id."""
        response = self.client.post(DELETE_ACTION, {"store_id": "abcd"})
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 500)
        self.assertEqual(
            content, b"Unexpected Error: Request Failed due to store_id being invalid."
        )

    def test_delete_page_invalid_store_id(self) -> None:
        """Test the delete page with the invalid store id."""
        response = self.client.get("/stores/delete/99999")
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 404)
        self.assertEqual(content, b"Store does not exist.")

    def test_delete_page_when_not_logged_in(self) -> None:
        """Test the delete page when not logged in."""
        self.client.logout()
        response = self.client.get(f"/stores/delete/{self.store.id}")
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_delete_page_invalid_method(self) -> None:
        """Test the delete page with a invalid HTTP method."""
        response = self.client.post(f"/stores/delete/{self.store.id}")
        status_code = response.status_code

        self.assertEqual(status_code, 405)
