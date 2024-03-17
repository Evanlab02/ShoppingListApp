"""Contains tests for the item create view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from items.models import ShoppingItem as Item
from items.views import CREATE_ACTION, CREATE_PAGE
from stores.models import ShoppingStore as Store

MOCK_ITEM_NAME = "Crumbed Chicken"


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
        self.store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        self.item = Item.objects.create(
            name=MOCK_ITEM_NAME,
            description="",
            price=2500,
            store=self.store,
            user=self.user,
        )
        self.item.save()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        Item.objects.all().delete()
        Store.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    def test_get_create_page(self) -> None:
        """Test the create page."""
        response = self.client.get(f"/items/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/create.html")

    def test_get_create_page_not_logged_in(self) -> None:
        """Test the create page when not logged in."""
        self.client.logout()
        response = self.client.get(f"/items/{CREATE_PAGE}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page_when_not_logged_in(self) -> None:
        """Test the create page action when not logged in."""
        self.client.logout()
        response = self.client.post(f"/items/{CREATE_ACTION}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_post_create_page(self) -> None:
        """Test the create page action."""
        response = self.client.post(
            f"/items/{CREATE_ACTION}",
            {
                "store-input": f"{self.store.id}",
                "description-input": "test",
                "price-input": "1000",
                "item-input": "Sony Headphones",
            },
        )

        item = Item.objects.get(name="Sony Headphones")

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"/items/detail/{item.id}", 302, 404)

    def test_post_create_page_existing_name(self) -> None:
        """Test the create page action with an existing name."""
        response = self.client.post(
            f"/items/{CREATE_ACTION}",
            {
                "store-input": f"{self.store.id}",
                "description-input": "test",
                "price-input": "1000",
                "item-input": MOCK_ITEM_NAME,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/items/create?error=Item Already Exists.", 302, 200)

    def test_post_create_page_invalid_store_id(self) -> None:
        """Test the create page action with an invalid payload."""
        response = self.client.post(
            f"/items/{CREATE_ACTION}",
            {
                "store-input": "abcde",
                "description-input": "test",
                "price-input": "1000",
                "item-input": MOCK_ITEM_NAME,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/items/create?error=Validation failed, please try again.",
            302,
            200,
        )

    def test_post_create_page_invalid_store_price(self) -> None:
        """Test the create page action with an invalid payload."""
        response = self.client.post(
            f"/items/{CREATE_ACTION}",
            {
                "store-input": f"{self.store.id}",
                "description-input": "test",
                "price-input": "abcd",
                "item-input": MOCK_ITEM_NAME,
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/items/create?error=Validation failed, please try again.",
            302,
            200,
        )

    def test_post_create_page_invalid_payload(self) -> None:
        """Test the create page action with an invalid payload."""
        response = self.client.post(f"/items/{CREATE_ACTION}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            "/items/create?error=Validation failed, please try again.",
            302,
            200,
        )
