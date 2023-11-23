"""Contains tests for the item create view."""

import pytest

from shoppingitem.models import ShoppingStore

from ..helpers import DjangoClient, TestCase, create_test_user, does_match_base_criteria

ITEMS_CREATE_VIEW = "/items/create"


class TestItemCreateView(TestCase):
    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.client = DjangoClient()
        self.user = create_test_user()
        self.client.force_login(self.user)
        self.store = ShoppingStore.objects.create(
            name="Test Store",
            description="Test Description",
            store_type=1,
            user=self.user,
        )
        self.store.save()
        self.response = self.client.get(ITEMS_CREATE_VIEW)

    def test_response(self) -> None:
        """Test that the response matches all criteria."""
        does_match_base_criteria(self, self.response)

        # Template used is items/item_create.html
        self.assertTemplateUsed(self.response, "items/item_create.html")