"""Contains tests for the store repository functions."""

from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import create_store
from stores.models import ShoppingStore

TEST_STORE = "Test User Store"
TEST_DESCRIPTION = "This is a test store."


class TestStoreRepoCreate(TestCase):
    """Store repository tests."""

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
            name="Base Test Store",
            store_type=3,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        ShoppingStore.objects.all().delete()
        return super().tearDown()

    async def test_create_store(self) -> None:
        """Test create_store."""
        name = TEST_STORE
        store_type = 1
        description = TEST_DESCRIPTION
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
