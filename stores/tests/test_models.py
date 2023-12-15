"""Contains tests for the models in the stores app."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.models import ShoppingStore


class TestStoreModel(TestCase):
    """Tests for the ShoppingStore model."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.user.save()
        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        ShoppingStore.objects.all().delete()
        return super().tearDown()

    def test_str_method(self) -> None:
        """Test the __str__ method of the ShoppingStore model."""
        store = ShoppingStore.objects.create(
            name="Test Store", store_type=1, user=self.user
        )
        store.save()
        self.assertEqual(str(store), "Test Store")
