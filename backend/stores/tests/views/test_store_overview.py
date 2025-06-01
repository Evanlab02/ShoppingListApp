"""Test the store overview view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from stores.tests.factory import StoreFactory


class TestStoreOverviewView(TestCase):
    """Test the store overview view."""

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

    def test_get_overview_page(self) -> None:
        """Test get overview page."""
        response = self.client.get(reverse("store_overview_page"))
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")

    def test_get_overview_page_not_logged_in(self) -> None:
        """Test get overview page when not logged in."""
        self.client.logout()
        response = self.client.get(reverse("store_overview_page"))
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_get_personal_overview_page(self) -> None:
        """Test get personal overview page."""
        response = self.client.get(reverse("store_personal_overview_page"))
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")

    def test_personal_overview_page_not_accessible_when_logged_out(self) -> None:
        """Test personal overview page is not accessible when logged out."""
        self.client.logout()
        response = self.client.get(reverse("store_personal_overview_page"))
        status_code = response.status_code

        self.assertEqual(status_code, 302)
        self.assertRedirects(
            response=response,
            expected_url="/?error=You must be logged in to access that page.",
            status_code=302,
            target_status_code=200,
        )

    def test_get_overview_page_with_custom_page_number(self) -> None:
        """Test get overview page with custom page number."""
        response = self.client.get(reverse("store_overview_page"), {"page": 2})
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")

    def test_get_overview_page_with_custom_limit(self) -> None:
        """Test get overview page with custom limit."""
        response = self.client.get(reverse("store_overview_page"), {"limit": 5})
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")

    def test_get_overview_page_with_invalid_page_number(self) -> None:
        """Test get overview page with invalid page number."""
        response = self.client.get(reverse("store_overview_page"), {"page": "invalid"})
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")

    def test_get_overview_page_with_invalid_limit(self) -> None:
        """Test get overview page with invalid limit."""
        response = self.client.get(reverse("store_overview_page"), {"limit": "invalid"})
        status_code = response.status_code

        self.assertEqual(status_code, 200)
        self.assertTemplateUsed(response=response, template_name="stores/overview.html")
