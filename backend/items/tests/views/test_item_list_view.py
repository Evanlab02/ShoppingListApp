"""Contains tests for the item list views."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory


class TestItemListView(TestCase):
    """Tests for the item list views."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = Client()
        self.user = UserFactory.create()

        self.items = ItemFactory.create_batch(size=15, user=self.user)
        self.non_personal_items = ItemFactory.create_batch(size=15)

        self.total_price_personal = sum(item.price for item in self.items)
        self.total_price_non_personal = sum(item.price for item in self.non_personal_items)
        self.total_price = self.total_price_personal + self.total_price_non_personal

        self.average_price_personal = self.total_price_personal / len(self.items)
        self.average_price_non_personal = self.total_price_non_personal / len(
            self.non_personal_items
        )
        self.average_price = self.total_price / (len(self.items) + len(self.non_personal_items))

        self.max_price_personal = max(item.price for item in self.items)
        self.max_price_non_personal = max(item.price for item in self.non_personal_items)
        self.max_price = max(self.max_price_personal, self.max_price_non_personal)

        self.min_price_personal = min(item.price for item in self.items)
        self.min_price_non_personal = min(item.price for item in self.non_personal_items)
        self.min_price = min(self.min_price_personal, self.min_price_non_personal)

        self.client.force_login(self.user)
        self.url = reverse("item_overview_page")
        self.personal_url = reverse("item_personalized_overview_page")

    def test_item_list_view(self) -> None:
        """Test the item list view."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/overview.html")

        # Base Context
        context = response.context
        self.assertEqual(context["page_title"], "All Items")
        self.assertFalse(context["is_personal"])
        self.assertTrue(context["is_overview"])
        self.assertTrue(context["show_advanced_navigation"])

        # Pagination Context
        pagination = context["pagination"]
        self.assertEqual(pagination["total"], 30)
        self.assertEqual(pagination["page_number"], 1)
        self.assertEqual(pagination["total_pages"], 3)
        self.assertFalse(pagination["has_previous"])
        self.assertIsNone(pagination["previous_page"])
        self.assertTrue(pagination["has_next"])
        self.assertEqual(pagination["next_page"], 2)

        # Aggregation Context
        aggregation = context["aggregation"]
        self.assertEqual(aggregation["total_items"], 30)
        self.assertEqual(aggregation["total_price"], self.total_price)
        self.assertEqual(aggregation["average_price"], self.average_price)
        self.assertEqual(aggregation["max_price"], self.max_price)
        self.assertEqual(aggregation["min_price"], self.min_price)

    def test_item_list_view_personal(self) -> None:
        """Test the item list view for a personal user."""
        self.client.force_login(self.user)

        response = self.client.get(self.personal_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/overview.html")

        # Base Context
        context = response.context
        self.assertEqual(context["page_title"], "Your Items")
        self.assertTrue(context["is_personal"])
        self.assertTrue(context["is_overview"])
        self.assertTrue(context["show_advanced_navigation"])

        # Pagination Context
        pagination = context["pagination"]
        self.assertEqual(pagination["total"], 15)
        self.assertEqual(pagination["page_number"], 1)
        self.assertEqual(pagination["total_pages"], 2)
        self.assertFalse(pagination["has_previous"])
        self.assertIsNone(pagination["previous_page"])
        self.assertTrue(pagination["has_next"])
        self.assertEqual(pagination["next_page"], 2)

        # Aggregation Context
        aggregation = context["aggregation"]
        self.assertEqual(aggregation["total_items"], 15)
        self.assertEqual(aggregation["total_price"], self.total_price_personal)
        self.assertEqual(aggregation["average_price"], self.average_price_personal)
        self.assertEqual(aggregation["max_price"], self.max_price_personal)
        self.assertEqual(aggregation["min_price"], self.min_price_personal)

    def test_item_list_view_pagination_between_pages(self) -> None:
        """Test the item list view pagination between pages."""
        self.client.force_login(self.user)

        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/overview.html")

        # Base Context
        context = response.context
        self.assertEqual(context["page_title"], "All Items")
        self.assertFalse(context["is_personal"])
        self.assertTrue(context["is_overview"])
        self.assertTrue(context["show_advanced_navigation"])

        # Pagination Context
        pagination = context["pagination"]
        self.assertEqual(pagination["total"], 30)
        self.assertEqual(pagination["page_number"], 2)
        self.assertEqual(pagination["total_pages"], 3)
        self.assertTrue(pagination["has_previous"])
        self.assertEqual(pagination["previous_page"], 1)
        self.assertTrue(pagination["has_next"])
        self.assertEqual(pagination["next_page"], 3)

        # Aggregation Context
        aggregation = context["aggregation"]
        self.assertEqual(aggregation["total_items"], 30)
        self.assertEqual(aggregation["total_price"], self.total_price)
        self.assertEqual(aggregation["average_price"], self.average_price)
        self.assertEqual(aggregation["max_price"], self.max_price)
        self.assertEqual(aggregation["min_price"], self.min_price)

    def test_item_list_view_pagination_last_page(self) -> None:
        """Test the item list view pagination on the last page."""
        self.client.force_login(self.user)

        response = self.client.get(f"{self.url}?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/overview.html")

        # Base Context
        context = response.context
        self.assertEqual(context["page_title"], "All Items")
        self.assertFalse(context["is_personal"])
        self.assertTrue(context["is_overview"])
        self.assertTrue(context["show_advanced_navigation"])

        # Pagination Context
        pagination = context["pagination"]
        self.assertEqual(pagination["total"], 30)
        self.assertEqual(pagination["page_number"], 3)
        self.assertEqual(pagination["total_pages"], 3)
        self.assertTrue(pagination["has_previous"])
        self.assertEqual(pagination["previous_page"], 2)
        self.assertFalse(pagination["has_next"])
        self.assertIsNone(pagination["next_page"])

        # Aggregation Context
        aggregation = context["aggregation"]
        self.assertEqual(aggregation["total_items"], 30)
        self.assertEqual(aggregation["total_price"], self.total_price)
        self.assertEqual(aggregation["average_price"], self.average_price)
        self.assertEqual(aggregation["max_price"], self.max_price)
        self.assertEqual(aggregation["min_price"], self.min_price)

    def test_item_list_view_requires_get_request(self) -> None:
        """Test the item list view requires a GET request."""
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)

    def test_item_list_view_requires_login(self) -> None:
        """Test the item list view requires a login."""
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_personal_item_list_view_requires_get_request(self) -> None:
        """Test the personal item list view requires a GET request."""
        response = self.client.post(self.personal_url)
        self.assertEqual(response.status_code, 405)

    def test_personal_item_list_view_requires_login(self) -> None:
        """Test the personal item list view requires a login."""
        self.client.logout()
        response = self.client.get(self.personal_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )
