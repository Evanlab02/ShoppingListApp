"""Contains the tests for the item create view."""

from uuid import uuid4

from django.test import Client, TestCase
from django.urls import reverse

from authentication.tests.factory import UserFactory
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.tests.factory import StoreFactory


class TestItemCreateView(TestCase):
    """Test the item create view."""

    def setUp(self) -> None:
        """Set up the test environment."""
        self.client = Client()
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.url = reverse("item_create_page")
        self.stores = StoreFactory.create_batch(20)

    def test_item_create_view_status_code_and_template(self) -> None:
        """
        Test the item create view.

        Given: A user is logged in.
        When: The user visits the item create page.
        Then: The user should see the item create page.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/create.html")

    def test_item_create_view_context(self) -> None:
        """
        Test the item create view context.

        Given: A user is logged in.
        When: The user visits the item create page.
        Then: The user should see the the form with all the correct fields
        """
        response = self.client.get(self.url)
        context = response.context

        # Base Context
        self.assertEqual(context["page_title"], "Create Item")
        self.assertEqual(context["is_personal"], False)
        self.assertEqual(context["is_overview"], False)
        self.assertEqual(context["show_advanced_navigation"], False)
        self.assertEqual(context["error"], None)

        # View Specific Context
        # Stores
        form = context["form"]
        form_stores = form.fields["store"].queryset.all()

        ids_of_stores_in_context = [store.id for store in form_stores]
        ids_of_stores_in_db = [store.id for store in self.stores]

        ids_of_stores_in_context.sort()
        ids_of_stores_in_db.sort()

        self.assertEqual(ids_of_stores_in_context, ids_of_stores_in_db)

        # Other fields
        self.assertIn("name", form.fields)
        self.assertIn("description", form.fields)
        self.assertIn("price", form.fields)

    def test_item_create_view_post(self) -> None:
        """
        Test the item create view with a POST request.

        Given: A user is logged in.
        When: The user submits a valid form.
        Then: The user should be redirected to the item detail page.
        And: The item should be created in the database.
        """
        uuid = uuid4().hex
        data = {
            "name": f"Test Item {uuid}",
            "store": f"{self.stores[0].id}",
            "price": 100,
            "description": "Test Description",
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)

        item = Item.objects.get(name=f"Test Item {uuid}")
        self.assertRedirects(response, reverse("item_detail_page", kwargs={"item_id": item.id}))

    def test_item_create_view_needs_login(self) -> None:
        """
        Test the item create view needs a login.

        Given: A user is not logged in.
        When: The user visits the item create page.
        Then: The user should be redirected to the login page.
        """
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_item_create_view_missing_fields(self) -> None:
        """
        Test the item create view with missing fields.

        Given: A user is logged in.
        When: The user submits a form with missing fields.
        Then: The user should see form errors for the missing fields.
        """
        data = {
            "name": "Test Item",
            "store": f"{self.stores[0].id}",
            "price": "",
            "description": "",
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["price"], ["This field is required."])

    def test_item_create_view_invalid_fields(self) -> None:
        """
        Test the item create view with an invalid price.

        Given: A user is logged in.
        When: The user submits a form with a invalid price.
        Then: The user should see a form error for the invalid price.
        """
        data = {
            "name": "Test Item",
            "store": f"{self.stores[0].id}",
            "price": "not a number",
            "description": "Test Description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["price"], ["Enter a number."])

    def test_item_create_view_item_already_exists(self) -> None:
        """
        Test the item create view with an item that already exists.

        Given: A user is logged in.
        When: The user submits a form with an item that already exists.
        Then: The user should see an error message.
        """
        ItemFactory.create(name="Test Item", store=self.stores[0], user=self.user)
        data = {
            "name": "Test Item",
            "store": f"{self.stores[0].id}",
            "price": 100,
            "description": "Test Description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertEqual(form.errors["name"], ["Item with this name already exists in this store."])

    def test_item_create_view_store_does_not_exist(self) -> None:
        """
        Test the item create view with a store that does not exist.

        Given: A user is logged in.
        When: The user submits a form with a store that does not exist.
        Then: The user should see an error message.
        """
        data = {
            "name": "Test Item",
            "store": 999999,
            "price": 100,
            "description": "Test Description",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)

        form = response.context["form"]
        self.assertIn("store", form.errors)
