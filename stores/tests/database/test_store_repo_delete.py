"""Contains tests for the store repository functions."""


import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import delete_store
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

    async def test_delete_store(self) -> None:
        """Test delete_store."""
        await delete_store(self.store.id, self.user)
        store_exists = await ShoppingStore.objects.filter(id=self.store.id).aexists()
        self.assertFalse(store_exists)

    async def test_delete_store_invalid_id(self) -> None:
        """Test delete_store with an invalid id."""
        with self.assertRaises(ShoppingStore.DoesNotExist):
            await delete_store(100, self.user)
        store_exists = await ShoppingStore.objects.filter(id=self.store.id).aexists()
        self.assertTrue(store_exists)

    async def test_delete_store_invalid_user(self) -> None:
        """Test delete_store with an invalid user."""
        user = await User.objects.acreate(
            username="testuser2",
            email="testuser2@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        await user.asave()

        with self.assertRaises(ShoppingStore.DoesNotExist):
            await delete_store(self.store.id, user)

        store_exists = await ShoppingStore.objects.filter(id=self.store.id).aexists()
        self.assertTrue(store_exists)
