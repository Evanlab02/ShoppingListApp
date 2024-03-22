"""Contains tests for the item router get items endpoint."""

from django.contrib.auth.models import User
from django.test.client import Client
from django.test.testcases import TestCase

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store


class TestGetItemsEndpoint(TestCase):
    """Test the get items endpoint."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
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
            name="Test Item",
            description="Test Description",
            price=100,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        self.alt_item = Item.objects.create(
            name="Alternate Item",
            description="Alternate Description",
            price=200,
            store=self.store,
            user=self.user,
        )
        self.alt_item.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    def test_get_items(self) -> None:
        """Test getting all items."""
        response = self.client.get("/api/v1/items")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertIn("items", data)
        self.assertIn("total", data)
        self.assertIn("page_number", data)
        self.assertIn("total_pages", data)
        self.assertIn("has_previous", data)
        self.assertIn("previous_page", data)
        self.assertIn("has_next", data)
        self.assertIn("next_page", data)

        self.assertEqual(data.get("total"), 2)
        self.assertEqual(data.get("page_number"), 1)
        self.assertEqual(data.get("total_pages"), 1)
        self.assertEqual(data.get("has_previous"), False)
        self.assertEqual(data.get("previous_page"), None)
        self.assertEqual(data.get("has_next"), False)
        self.assertEqual(data.get("next_page"), None)

        items = data.get("items")
        self.assertEqual(len(items), 2)
        self.assertEqual(items[1].get("name"), "Test Item")
        self.assertEqual(items[0].get("name"), "Alternate Item")
        self.assertEqual(items[1].get("description"), "Test Description")
        self.assertEqual(items[0].get("description"), "Alternate Description")
        self.assertEqual(items[1].get("price"), "100.00")
        self.assertEqual(items[0].get("price"), "200.00")
        self.assertEqual(items[1].get("store").get("name"), "Base Test Store")
        self.assertEqual(items[0].get("store").get("name"), "Base Test Store")
        self.assertEqual(items[1].get("user").get("username"), "testuser")
        self.assertEqual(items[0].get("user").get("username"), "testuser")

    def test_get_items_page_1(self) -> None:
        """Test getting all items on page 1."""
        response = self.client.get("/api/v1/items?page=1&per_page=1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data.get("total"), 2)
        self.assertEqual(data.get("page_number"), 1)
        self.assertEqual(data.get("total_pages"), 2)
        self.assertEqual(data.get("has_previous"), False)
        self.assertEqual(data.get("previous_page"), None)
        self.assertEqual(data.get("has_next"), True)
        self.assertEqual(data.get("next_page"), 2)
        items = data.get("items")
        self.assertEqual(len(items), 1)

    def test_get_items_page_2(self) -> None:
        """Test getting all items on page 2."""
        response = self.client.get("/api/v1/items?page=2&per_page=1")
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data.get("total"), 2)
        self.assertEqual(data.get("page_number"), 2)
        self.assertEqual(data.get("total_pages"), 2)
        self.assertEqual(data.get("has_previous"), True)
        self.assertEqual(data.get("previous_page"), 1)
        self.assertEqual(data.get("has_next"), False)
        self.assertEqual(data.get("next_page"), None)
        items = data.get("items")
        self.assertEqual(len(items), 1)
