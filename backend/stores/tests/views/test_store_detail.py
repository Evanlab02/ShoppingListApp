"""Test the store detail view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from stores.tests.factory import StoreFactory


class TestStoreDetailView(TestCase):
    """Test the store detail view."""

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

    def test_get_detail_page(self) -> None:
        """Test get detail page."""
        response = self.client.get(reverse("store_detail_page", kwargs={"store_id": self.store.id}))
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/detail.html")

    def test_get_detail_page_not_logged_in(self) -> None:
        """Test get detail page when not logged in."""
        self.client.logout()
        response = self.client.get(reverse("store_detail_page", kwargs={"store_id": self.store.id}))
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_get_detail_page_invalid_store_id(self) -> None:
        """Test get detail page with invalid store id."""
        response = self.client.get(reverse("store_detail_page", kwargs={"store_id": 99999}))
        status_code = response.status_code
        content = response.content

        self.assertEqual(status_code, 404)
        self.assertEqual(content, b"This store does not exist.")

    def test_get_detail_page_invalid_method(self) -> None:
        """Test get detail page with invalid HTTP method."""
        response = self.client.post(
            reverse("store_detail_page", kwargs={"store_id": self.store.id})
        )
        status_code = response.status_code

        self.assertEqual(status_code, 405)
