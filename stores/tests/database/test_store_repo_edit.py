"""Contains tests for the store repository functions."""


import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import edit_store
from stores.models import ShoppingStore

TEST_STORE = "Test User Store"
TEST_DESCRIPTION = "This is a test store."


class TestStoreRepoCreate(TestCase):
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

        self.store = ShoppingStore.objects.create(
            name=TEST_STORE,
            store_type=3,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()

        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        ShoppingStore.objects.all().delete()
        return super().tearDown()

    async def test_edit_store_name(self) -> None:
        """Test edit_store."""
        result = await edit_store(self.store.id, "New Edited Store")
        self.assertEqual(result.name, "New Edited Store")
        self.assertEqual(result.store_type, 3)
        self.assertEqual(result.description, TEST_DESCRIPTION)

    async def test_edit_store_type(self) -> None:
        """Test edit_store."""
        result = await edit_store(self.store.id, store_type=2)
        self.assertEqual(result.name, TEST_STORE)
        self.assertEqual(result.store_type, 2)
        self.assertEqual(result.description, TEST_DESCRIPTION)

    async def test_edit_store_description(self) -> None:
        """Test edit_store."""
        result = await edit_store(self.store.id, store_description="New Description")
        self.assertEqual(result.name, TEST_STORE)
        self.assertEqual(result.store_type, 3)
        self.assertEqual(result.description, "New Description")
