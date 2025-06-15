"""Contains the tests for the item update view."""

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestItemUpdateView(TestCase):
    """
    Test the item update view.

    Tests: items.views.update_page
    """

    def setUp(self) -> None:
        """
        Set up the test environment.

        1. Creates a client, user, and 20 stores.
        2. Creates an item for the user and the first store.
        3. Sets the URL for the item update view.
        """
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)

        self.stores = StoreFactory.create_batch(20)
        self.item = ItemFactory.create(user=self.user, store=self.stores[0])
        self.url = reverse("item_update_page", kwargs={"item_id": self.item.id})

    def test_item_update_view_get_status_code_and_template(self) -> None:
        """
        Test the item update view.

        Given: A user is logged in.
        When: The user visits the item update view.
        Then: The response is 200.
        And: The template used is "items/update.html".+
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/update.html")

    def test_item_update_view_get_context(self) -> None:
        """
        Test the item update view context.

        Given: A user is logged in.
        When: The user visits the item update view.
        Then: The context contains the page title and flags for navigation.
        And: The form data.
        """
        response = self.client.get(self.url)
        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], "Update Item")
        self.assertFalse(context["is_personal"])
        self.assertFalse(context["is_overview"])
        self.assertFalse(context["show_advanced_navigation"])

        # Form Context
        form = context["form"]
        self.assertEqual(form.initial["name"], self.item.name)
        self.assertEqual(form.initial["description"], self.item.description)
        self.assertEqual(form.initial["price"], self.item.price)
        self.assertEqual(form.initial["store"], self.item.store.id)
        self.assertEqual(form.user, self.user)

    def test_item_update_view_needs_login(self) -> None:
        """
        Test the item update view needs a login.

        Given: A user is logged out.
        When: The user visits the item update view.
        Then: The response is 302.
        And: The user is redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login_page')}?error=You must be logged in to access that page."
        )

    def test_item_update_with_invalid_item_id(self) -> None:
        """
        Test the item update view with an invalid item id.

        Given: A user is logged in.
        When: The user visits the item update view with an invalid item id.
        Then: The response is 404.
        """
        url = reverse("item_update_page", kwargs={"item_id": 999999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "dashboard/err/404.html")

    def test_item_update_view_post_redirects_to_detail_page(self) -> None:
        """
        Test the item update view post redirects to detail page.

        Given: A user is logged in.
        When: The user updates the item using a POST request.
        Then: The response is 302.
        And: The user is redirected to the item detail page.
        And: The item is updated with the new data.
        """
        response = self.client.post(
            self.url,
            data={
                "name": "Test Item",
                "store": self.stores[1].id,
                "price": 999888,
                "description": "Test Description",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('item_detail_page', kwargs={'item_id': self.item.id})}",
        )

        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.store, self.stores[1])
        self.assertEqual(self.item.price, 999888)
        self.assertEqual(self.item.description, "Test Description")

    def test_item_update_view_post_invalid_price(self) -> None:
        """
        Test the item update view post with an invalid price.

        Given: A user is logged in.
        When: The user updates the item using a POST request with an invalid price.
        Then: The form contains form errors indicating the price is invalid.
        """
        response = self.client.post(
            self.url,
            data={
                "name": "Test Item",
                "store": self.stores[1].id,
                "price": "not a number",
                "description": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["price"], ["Enter a number."])

    def test_item_update_view_post_empty_name(self) -> None:
        """
        Test the item update view post with an empty name.

        Given: A user is logged in.
        When: The user updates the item using a POST request with an empty name.
        Then: The form contains form errors indicating the name is required.
        """
        response = self.client.post(
            self.url,
            data={
                "name": "",
                "store": self.stores[1].id,
                "price": 999888,
                "description": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["name"], ["This field is required."])

    def test_item_update_view_post_with_item_already_exists(self) -> None:
        """
        Test the item update view post with an item that already exists.

        Given: A user is logged in.
        When: The user updates the item using a POST request with an item that already exists.
        Then: The form contains form errors indicating the item already exists.
        """
        ItemFactory.create(user=self.user, store=self.stores[1], name="Test Item")
        response = self.client.post(
            self.url,
            data={
                "name": "Test Item",
                "store": self.stores[1].id,
                "price": 999888,
                "description": "Test Description",
            },
        )
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["name"], ["Item with this name already exists in this store."])
