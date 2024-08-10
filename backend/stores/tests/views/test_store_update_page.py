"""Test the store update view."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE_NAME = "Test Store"


class TestStoreUpdateView(TestCase):
    """Test the store update view."""

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

    def test_update_page(self) -> None:
        """Test the update page."""
        response = self.client.get(f"/stores/update/{self.store.id}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stores/update.html")

    def test_update_page_when_logged_out(self) -> None:
        """Test the update page."""
        self.client.logout()
        response = self.client.get(f"/stores/update/{self.store.id}")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "/?error=You must be logged in to access that page.", 302, 200
        )

    def test_update_page_invalid_id(self) -> None:
        """Test the update page with invalid id."""
        response = self.client.get("/stores/update/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Store does not exist.")

    def test_update_action(self) -> None:
        """Test the update action route."""
        response = self.client.post(f"/stores/update/action/{self.store.id}")
        self.assertRedirects(response, f"/stores/detail/{self.store.id}", 302, 200)
        self.assertEqual(self.store.name, TEST_STORE_NAME)
        self.assertEqual(self.store.description, "Test Description")
        self.assertEqual(self.store.store_type, 3)

    def test_update_action_with_body(self) -> None:
        """Test the update action route with body."""
        response = self.client.post(
            f"/stores/update/action/{self.store.id}", {"store-input": "Hello World"}
        )
        self.store.refresh_from_db()
        self.assertRedirects(response, f"/stores/detail/{self.store.id}", 302, 200)
        self.assertEqual(self.store.name, "Hello World")

    def test_update_action_with_existing_name(self) -> None:
        """Test the update action route with existing name."""
        response = self.client.post(
            f"/stores/update/action/{self.store.id}", {"store-input": TEST_STORE_NAME}
        )
        self.assertRedirects(
            response,
            f"/stores/update/{self.store.id}?error=Store 'Test Store' already exists.",
        )

    def test_update_action_with_invalid_type_integer(self) -> None:
        """Test the update action route with invalid type integer."""
        response = self.client.post(
            f"/stores/update/action/{self.store.id}", {"store-type-input": 4}
        )
        self.assertRedirects(
            response,
            f"/stores/update/{self.store.id}?error=Internal Conversion Error: Store Type Could Not Be Converted To String.",  # noqa: E501
        )

    def test_update_action_with_invalid_type_string(self) -> None:
        """Test the update action route with invalid type string."""
        response = self.client.post(
            f"/stores/update/action/{self.store.id}", {"store-type-input": "Unknown"}
        )
        self.assertRedirects(
            response,
            f"/stores/update/{self.store.id}?error=Store type 'Unknown' is invalid.",  # noqa: E501
        )

    def test_update_action_with_invaid_id(self) -> None:
        """Test the update action route with invalid store id."""
        response = self.client.post("/stores/update/action/9999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content, b"Store does not exist or does not belong to you.")
