"""Contains tests for the store create view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestStoreCreateView(TestCase):
    """Test the store create view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_get_create_page(self) -> None:
        """Test the create page."""
        response = self.client.get(reverse("store_create_page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/create.html")

    def test_get_create_page_not_logged_in(self) -> None:
        """Test the create page when not logged in."""
        self.client.logout()
        response = self.client.get(reverse("store_create_page"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page_when_not_logged_in(self) -> None:
        """Test the create page action when not logged in."""
        self.client.logout()
        response = self.client.post(reverse("store_create_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page(self) -> None:
        """Test the create page action."""
        response = self.client.post(
            reverse("store_create_action"),
            {
                "store-input": "test",
                "description-input": "test",
                "store-type-input": "Online",
            },
        )
        store = Store.objects.get(name="test")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, reverse("store_detail_page", kwargs={"store_id": store.id}), 302, 200
        )

    def test_post_create_page_existing_name(self) -> None:
        """Test the create page action with an existing name."""
        StoreFactory.create(name="test", user=self.user)

        response = self.client.post(
            reverse("store_create_action"),
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
            reverse("store_create_action"),
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
        response = self.client.post(reverse("store_create_action"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/stores/create?error=Store name and type are required.",
            302,
            200,
        )
