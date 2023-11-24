"""Contains tests for the item create view."""

import pytest

from ..helpers import DjangoClient, TestCase, create_test_user, does_match_base_criteria

STORE_CREATE_VIEW = "/items/stores/create"


class TestStoreCreateView(TestCase):
    """Test the store create view."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.client = DjangoClient()
        self.user = create_test_user()
        self.client.force_login(self.user)
        self.response = self.client.get(STORE_CREATE_VIEW)

    def test_response(self) -> None:
        """Test that the response matches all criteria."""
        does_match_base_criteria(self, self.response)
        self.assertTemplateUsed(self.response, "items/store_create.html")
