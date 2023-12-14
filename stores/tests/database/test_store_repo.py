"""Contains tests for the store repository functions."""


import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import create_store
from stores.models import ShoppingStore


class TestStoreRepo(TestCase):
    """Store repository tests."""

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

    async def test_create_store(self) -> None:
        """Test create_store."""
        name = "Test Creation Store"
        store_type = 1
        description = "This is a test store."
        store = await create_store(
            name,
            store_type,
            description,
            self.user,
        )
        self.assertIsInstance(store, ShoppingStore)
        self.assertEqual(store.name, name)
        self.assertEqual(store.store_type, store_type)
        self.assertEqual(store.description, description)
        self.assertEqual(store.user, self.user)
