"""Contains tests for the store repository."""

import pytest

from shoppingitem.database import StoreRepository
from shoppingitem.models import ShoppingStore

from ..helpers import (
    TestCase,
    create_secondary_test_user,
    create_test_user,
    create_test_user_client,
)

TEST_STORE = "Test Store"
TEST_DESCRIPTION = "Test Description"
ALT_TEST_STORE = "Test Store 2"
ALT_TEST_DESCRIPTION = "Test Description 2"


class TestStoreRepo(TestCase):
    """Tests for the store repository."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.repo = StoreRepository()
        self.user = create_test_user()
        self.secondary_user = create_secondary_test_user()
        self.user_client = create_test_user_client(self.user)
        return super().setUp()

    def test_get_stores_for_user(self):
        """Test getting stores for a user."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        secondary_user_store = ShoppingStore.objects.create(
            name=ALT_TEST_STORE,
            user=self.secondary_user,
            description=ALT_TEST_DESCRIPTION,
            store_type=1,
        )
        secondary_user_store.save()

        stores = self.repo.get_all_stores_for_user(self.user)
        self.assertEqual(len(stores), 1)
        self.assertEqual(stores[0].name, TEST_STORE)
        self.assertEqual(stores[0].user, self.user)
        self.assertEqual(stores[0].description, TEST_DESCRIPTION)
        self.assertEqual(stores[0].store_type, 1)

    def test_get_all_stores(self):
        """Test getting all stores."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        secondary_user_store = ShoppingStore.objects.create(
            name=ALT_TEST_STORE,
            user=self.secondary_user,
            description=ALT_TEST_DESCRIPTION,
            store_type=2,
        )
        secondary_user_store.save()

        stores = self.repo.get_all_stores()
        self.assertEqual(len(stores), 2)
        self.assertEqual(stores[0].name, ALT_TEST_STORE)
        self.assertEqual(stores[0].user, self.secondary_user)
        self.assertEqual(stores[0].description, ALT_TEST_DESCRIPTION)
        self.assertEqual(stores[0].store_type, 2)
        self.assertEqual(stores[1].name, TEST_STORE)
        self.assertEqual(stores[1].user, self.user)
        self.assertEqual(stores[1].description, TEST_DESCRIPTION)
        self.assertEqual(stores[1].store_type, 1)

    def test_count_stores_by_type(self):
        """Test counting stores by type."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        for i in range(2, 4):
            secondary_user_store = ShoppingStore.objects.create(
                name=f"Test Store {i}",
                user=self.secondary_user,
                description=f"Test Description {i}",
                store_type=2,
            )
            secondary_user_store.save()

        for i in range(4, 7):
            secondary_user_store = ShoppingStore.objects.create(
                name=f"Test Store {i}",
                user=self.secondary_user,
                description=f"Test Description {i}",
                store_type=3,
            )
            secondary_user_store.save()

        count = self.repo.count_stores_by_type(1)
        self.assertEqual(count, 1)

        count = self.repo.count_stores_by_type(2)
        self.assertEqual(count, 2)

        count = self.repo.count_stores_by_type(3)
        self.assertEqual(count, 3)

    def test_count_stores_by_type_for_user(self):
        """Test counting stores by type for a user."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        for i in range(2, 4):
            secondary_user_store = ShoppingStore.objects.create(
                name=f"Test Store {i}",
                user=self.secondary_user,
                description=f"Test Description {i}",
                store_type=2,
            )
            secondary_user_store.save()

        for i in range(4, 7):
            secondary_user_store = ShoppingStore.objects.create(
                name=f"Test Store {i}",
                user=self.secondary_user,
                description=f"Test Description {i}",
                store_type=3,
            )
            secondary_user_store.save()

        count = self.repo.count_stores_by_type_for_user(1, self.user)
        self.assertEqual(count, 1)

        count = self.repo.count_stores_by_type_for_user(2, self.user)
        self.assertEqual(count, 0)

        count = self.repo.count_stores_by_type_for_user(3, self.user)
        self.assertEqual(count, 0)

        count = self.repo.count_stores_by_type_for_user(1, self.secondary_user)
        self.assertEqual(count, 0)

        count = self.repo.count_stores_by_type_for_user(2, self.secondary_user)
        self.assertEqual(count, 2)

        count = self.repo.count_stores_by_type_for_user(3, self.secondary_user)
        self.assertEqual(count, 3)

    def test_get_store_by_id(self):
        """Test getting a store by id."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        secondary_user_store = ShoppingStore.objects.create(
            name=ALT_TEST_STORE,
            user=self.secondary_user,
            description=ALT_TEST_DESCRIPTION,
            store_type=2,
        )
        secondary_user_store.save()

        store = self.repo.get_store_by_id(user_store.id)
        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        store = self.repo.get_store_by_id(secondary_user_store.id)
        self.assertEqual(store.name, ALT_TEST_STORE)
        self.assertEqual(store.user, self.secondary_user)
        self.assertEqual(store.description, ALT_TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 2)

    def test_get_store_by_name(self):
        """Test getting a store by name."""
        user_store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        user_store.save()

        secondary_user_store = ShoppingStore.objects.create(
            name=ALT_TEST_STORE,
            user=self.secondary_user,
            description=ALT_TEST_DESCRIPTION,
            store_type=2,
        )
        secondary_user_store.save()

        store = self.repo.get_store_by_name(TEST_STORE)
        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        store = self.repo.get_store_by_name(ALT_TEST_STORE)
        self.assertEqual(store.name, ALT_TEST_STORE)
        self.assertEqual(store.user, self.secondary_user)
        self.assertEqual(store.description, ALT_TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 2)

    def test_create_store(self):
        """Test creating a store."""
        store = self.repo.create_store(
            name=TEST_STORE, description=TEST_DESCRIPTION, store_type=1, user=self.user
        )

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

    def test_does_store_exist_should_return_true(self):
        """Test does store exist should return true."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertTrue(self.repo.does_store_exist(TEST_STORE))

    def test_does_store_exist_should_return_false(self):
        """Test does store exist should return false."""
        self.assertFalse(self.repo.does_store_exist(TEST_STORE))

    def test_create_store_should_fail_with_duplicate(self):
        """Test creating a store should fail with duplicate."""
        store = self.repo.create_store(
            name=TEST_STORE, description=TEST_DESCRIPTION, store_type=1, user=self.user
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        with self.assertRaises(ValueError):
            self.repo.create_store(
                name=TEST_STORE,
                description=TEST_DESCRIPTION,
                store_type=1,
                user=self.user,
            )

    def test_create_store_with_invalid_type(self):
        """Test creating a store with an invalid type."""
        with self.assertRaises(ValueError):
            self.repo.create_store(
                name=TEST_STORE,
                description=TEST_DESCRIPTION,
                store_type=4,
                user=self.user,
            )

    def test_create_store_with_invalid_type_string(self):
        """Test creating a store with an invalid type string."""
        with self.assertRaises(TypeError):
            self.repo.create_store(
                name=TEST_STORE,
                description=TEST_DESCRIPTION,
                store_type="1",
                user=self.user,
            )

    def test_edit_store(self):
        """Test editing a store."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        self.repo.edit_store(
            store_id=store.id,
            name=ALT_TEST_STORE,
            description=ALT_TEST_DESCRIPTION,
            store_type=2,
        )

        store.refresh_from_db()

        self.assertEqual(store.name, ALT_TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, ALT_TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 2)

    def test_edit_store_to_existing_name(self):
        """Test editing a store to an existing name."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        secondary_store = ShoppingStore.objects.create(
            name=ALT_TEST_STORE,
            user=self.user,
            description=ALT_TEST_DESCRIPTION,
            store_type=2,
        )
        secondary_store.save()

        self.assertEqual(secondary_store.name, ALT_TEST_STORE)
        self.assertEqual(secondary_store.user, self.user)
        self.assertEqual(secondary_store.description, ALT_TEST_DESCRIPTION)
        self.assertEqual(secondary_store.store_type, 2)

        with self.assertRaises(ValueError):
            self.repo.edit_store(
                store_id=store.id,
                name=ALT_TEST_STORE,
                description=ALT_TEST_DESCRIPTION,
                store_type=2,
            )

    def test_edit_store_empty_name(self):
        """Test editing a store with an empty name."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        with self.assertRaises(ValueError):
            self.repo.edit_store(
                store_id=store.id,
                name="",
                description=ALT_TEST_DESCRIPTION,
                store_type=2,
            )

    def test_edit_store_string_store_type(self):
        """Test editing a store with a string store type."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        with self.assertRaises(TypeError):
            self.repo.edit_store(
                store_id=store.id,
                name=ALT_TEST_STORE,
                description=ALT_TEST_DESCRIPTION,
                store_type="2",
            )

    def test_edit_store_invalid_store_type(self):
        """Test editing a store with an invalid store type."""
        store = ShoppingStore.objects.create(
            name=TEST_STORE,
            user=self.user,
            description=TEST_DESCRIPTION,
            store_type=1,
        )
        store.save()

        self.assertEqual(store.name, TEST_STORE)
        self.assertEqual(store.user, self.user)
        self.assertEqual(store.description, TEST_DESCRIPTION)
        self.assertEqual(store.store_type, 1)

        with self.assertRaises(ValueError):
            self.repo.edit_store(
                store_id=store.id,
                name=ALT_TEST_STORE,
                description=ALT_TEST_DESCRIPTION,
                store_type=0,
            )
