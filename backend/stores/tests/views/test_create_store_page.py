"""Contains tests for the store create view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store
from stores.views import CREATE_ACTION, CREATE_PAGE


class TestStoreCreateView(TestCase):
    """Test the store create view."""

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
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_create_page(self) -> None:
        """Test the create page."""
        response = self.client.get(f"/stores/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/create.html")

    def test_get_create_page_not_logged_in(self) -> None:
        """Test the create page when not logged in."""
        self.client.logout()
        response = self.client.get(f"/stores/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page_when_not_logged_in(self) -> None:
        """Test the create page action when not logged in."""
        self.client.logout()
        response = self.client.post(f"/stores/{CREATE_ACTION}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page(self) -> None:
        """Test the create page action."""
        response = self.client.post(
            f"/stores/{CREATE_ACTION}",
            {
                "store-input": "test",
                "description-input": "test",
                "store-type-input": "Online",
            },
        )
        store = Store.objects.get(name="test")
        store_id = store.id
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/stores/detail/{store_id}", 302, 200)

    def test_post_create_page_existing_name(self) -> None:
        """Test the create page action with an existing name."""
        response = self.client.post(
            f"/stores/{CREATE_ACTION}",
            {
                "store-input": "test",
                "description-input": "test",
                "store-type-input": "Online",
            },
        )
        store = Store.objects.get(name="test")
        store_id = store.id
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/stores/detail/{store_id}", 302, 200)

        response = self.client.post(
            f"/stores/{CREATE_ACTION}",
            {
                "store-input": "test",
                "description-input": "test",
                "store-type-input": "Online",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/stores/create?error=Store 'test' already exists.", 302, 200
        )

    def test_post_create_page_invalid_type(self) -> None:
        """Test the create page action with an invalid type."""
        response = self.client.post(
            f"/stores/{CREATE_ACTION}",
            {
                "store-input": "test",
                "description-input": "test",
                "store-type-input": "Invalid",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/stores/create?error=Store type 'Invalid' is invalid.", 302, 200
        )

    def test_post_create_page_invalid_payload(self) -> None:
        """Test the create page action when not logged in."""
        response = self.client.post(f"/stores/{CREATE_ACTION}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/stores/create?error=Store name and type are required.",
            302,
            200,
        )
