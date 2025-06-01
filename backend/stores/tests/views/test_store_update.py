"""Test the store update view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from stores.tests.factory import StoreFactory


class TestStoreUpdateView(TestCase):
    """Test the store update view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        """Tear down the test environment."""
        self.client.logout()
        return super().tearDown()

    def test_get_update_page(self) -> None:
        """Test get update page."""
        response = self.client.get(reverse("store_update_page", kwargs={"store_id": self.store.id}))
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/update.html")

    def test_get_update_page_not_logged_in(self) -> None:
        """Test get update page when not logged in."""
        self.client.logout()
        response = self.client.get(reverse("store_update_page", kwargs={"store_id": self.store.id}))
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_get_update_page_invalid_store_id(self) -> None:
        """Test get update page with invalid store id."""
        response = self.client.get(reverse("store_update_page", kwargs={"store_id": 99999}))
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 404)
        self.assertEqual(content, b"Store does not exist.")

    def test_get_update_page_invalid_method(self) -> None:
        """Test get update page with invalid HTTP method."""
        response = self.client.post(
            reverse("store_update_page", kwargs={"store_id": self.store.id})
        )
        status_code = response.status_code

        self.assertEqual(status_code, 405)

    def test_post_update_page(self) -> None:
        """Test post update page."""
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
            },
        )
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=reverse("store_detail_page", kwargs={"store_id": self.store.id}),
            status_code=302,
            target_status_code=200,
        )

    def test_post_update_page_not_logged_in(self) -> None:
        """Test post update page when not logged in."""
        self.client.logout()
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
            },
        )
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_post_update_page_invalid_store_id(self) -> None:
        """Test post update page with invalid store id."""
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": 99999}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
            },
        )
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 404)
        self.assertEqual(content, b"Store does not exist or does not belong to you.")

    def test_post_update_page_invalid_method(self) -> None:
        """Test post update page with invalid HTTP method."""
        response = self.client.get(
            reverse("store_update_action", kwargs={"store_id": self.store.id})
        )
        status_code = response.status_code

        self.assertEqual(status_code, 405)

    def test_post_update_page_with_store_type_conversion(self) -> None:
        """Test post update page with store type conversion."""
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
                "store-type-input": "2",
            },
        )
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=reverse("store_detail_page", kwargs={"store_id": self.store.id}),
            status_code=302,
            target_status_code=200,
        )

        self.store.refresh_from_db()
        self.assertEqual(self.store.store_type, 2)

    def test_post_update_page_with_invalid_store_type(self) -> None:
        """Test post update page with invalid store type."""
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
                "store-type-input": "invalid",
            },
        )
        status_code = response.status_code
        url = reverse("store_update_page", kwargs={"store_id": self.store.id})

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=f"{url}?error=Store type 'invalid' is invalid.",
            status_code=302,
            target_status_code=200,
        )

    def test_post_update_page_with_existing_store_name(self) -> None:
        """Test post update page with existing store name."""
        StoreFactory.create(user=self.user, name="Existing Store")
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "store-input": "Existing Store",
                "description-input": "Updated Description",
            },
        )
        status_code = response.status_code
        url = reverse("store_update_page", kwargs={"store_id": self.store.id})

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=f"{url}?error=Store 'Existing Store' already exists.",
            status_code=302,
            target_status_code=200,
        )

    def test_post_update_page_with_invalid_store_type_value(self) -> None:
        """Test post update page with invalid store type value."""
        response = self.client.post(
            reverse("store_update_action", kwargs={"store_id": self.store.id}),
            {
                "name": "Updated Store",
                "description": "Updated Description",
                "store-type-input": "4",
            },
        )
        status_code = response.status_code
        url = reverse("store_update_page", kwargs={"store_id": self.store.id})
        params = "?error=Internal Conversion Error: Store Type Could Not Be Converted To String."

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url=f"{url}{params}",
            status_code=302,
            target_status_code=200,
        )
