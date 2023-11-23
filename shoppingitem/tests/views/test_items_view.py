"""Contains tests for the items view."""

import pytest
from django.contrib.auth.models import User
from django.test import Client, TestCase

from ...models import ShoppingItem, ShoppingStore

TEST_EMAIL = "user@test.com"
FONT = '<link href="https://fonts.googleapis.com/css?family=Roboto&display=swap" rel="stylesheet">'
ITEMS_URL = "/items/"


class TestItemView(TestCase):
    """Test the items view."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self):
        """Set up the test environment."""
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email=TEST_EMAIL,
            password="testpassword",
            first_name="test",
            last_name="user",
        )
        self.user.save()
        self.client.login(username="testuser", password="testpassword")

    def test_view_with_no_items(self):
        """Test the user items view with no items."""
        response = self.client.get(ITEMS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/items_list_view.html")

    def test_item_view_with_items(self):
        """Tests the user items view with items."""
        store = ShoppingStore.objects.create(
            name="Test Store",
            store_type=1,
            description="Test Description",
            user=self.user,
        )
        store.save()

        item = ShoppingItem.objects.create(
            name="Test Item",
            store=store,
            price=10,
            user=self.user,
        )
        item.save()

        response = self.client.get(ITEMS_URL)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "items/items_list_view.html")

