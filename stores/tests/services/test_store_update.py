"""
Test store service - Update function.
"""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.errors.api_exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.models import ShoppingStore as Store
from stores.services import store_service

TEST_STORE = "Test Store Update"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description for test store."


class TestUpdatesStore(TestCase):
    """
    Test update store function.
    """

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testing123",
        )
        self.user.save()
        self.store = Store.objects.create(
            name=TEST_STORE,
            store_type=TEST_STORE_TYPE,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()
        return super().setUp()

    def tearDown(self) -> None:
        """Clean up after tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_update_store_with_no_values(self) -> None:
        """Test update store with no params."""
        await store_service.update_store(self.store.id, self.user)

        await self.store.arefresh_from_db()
        self.assertEqual(self.store.name, TEST_STORE)
        self.assertEqual(self.store.store_type, TEST_STORE_TYPE)
        self.assertEqual(self.store.description, TEST_DESCRIPTION)

    async def test_update_store_with_name(self) -> None:
        """Test update store with updated name."""
        new_store_name = "Updated Test Store"
        await store_service.update_store(self.store.id, self.user, new_store_name)

        await self.store.arefresh_from_db()
        self.assertEqual(self.store.name, new_store_name)

    async def test_update_store_with_type(self) -> None:
        """Test update store with updated type."""
        new_store_type = 3
        await store_service.update_store(self.store.id, self.user, None, new_store_type)

        await self.store.arefresh_from_db()
        self.assertEqual(self.store.store_type, new_store_type)

    async def test_update_store_with_description(self) -> None:
        """Test update store with updated description."""
        new_store_description = "Empty"
        await store_service.update_store(
            self.store.id, self.user, None, None, new_store_description
        )

        await self.store.arefresh_from_db()
        self.assertEqual(self.store.description, new_store_description)

    async def test_update_store_with_name_that_already_exists(self) -> None:
        """Test update store with name that already exists."""
        new_store_name = TEST_STORE

        with pytest.raises(StoreAlreadyExists):
            await store_service.update_store(self.store.id, self.user, new_store_name)

    async def test_update_store_with_invalid_store_type_number(self) -> None:
        """Test update store with store type number."""
        with pytest.raises(InvalidStoreType):
            await store_service.update_store(self.store.id, self.user, store_type=5)

    async def test_update_store_with_invalid_store_type_string(self) -> None:
        """Test update store with store type string."""
        with pytest.raises(InvalidStoreType):
            await store_service.update_store(self.store.id, self.user, store_type="Mac")

    async def test_update_store_with_invalid_id(self) -> None:
        with pytest.raises(StoreDoesNotExist):
            await store_service.update_store(9999, self.user, store_type=3)
