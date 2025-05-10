"""Test the store service functionality."""

from asgiref.sync import sync_to_async
from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.constants import STORE_TYPE_MAPPING
from stores.errors.exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.services.store_service import StoreService
from stores.tests.factory import StoreFactory


class TestStoreService(TestCase):
    """Test the store service functionality."""

    def setUp(self) -> None:
        """Set up the test."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.service = StoreService()

        self.create = sync_to_async(StoreFactory.create)

    async def test_update_store_name(self) -> None:
        """Test updating store name."""
        store = await self.service.update(
            store_id=self.store.id,
            user=self.user,
            store_name="New Name",
        )
        self.assertEqual(store.name, "New Name")
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(await store.auser(), self.user)

    async def test_update_store_type_with_int(self) -> None:
        """Test updating store type with integer value."""
        store = await self.service.update(
            store_id=self.store.id,
            user=self.user,
            store_type=3,
        )
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(await store.auser(), self.user)

    async def test_update_store_type_with_string(self) -> None:
        """Test updating store type with string value."""
        store_type_label = STORE_TYPE_MAPPING[3]
        store = await self.service.update(
            store_id=self.store.id,
            user=self.user,
            store_type=store_type_label,
        )
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, self.store.description)
        self.assertEqual(await store.auser(), self.user)

    async def test_update_store_description(self) -> None:
        """Test updating store description."""
        store = await self.service.update(
            store_id=self.store.id,
            user=self.user,
            store_description="New Description",
        )
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, "New Description")
        self.assertEqual(await store.auser(), self.user)

    async def test_update_store_all_fields(self) -> None:
        """Test updating all store fields."""
        store_type_label = STORE_TYPE_MAPPING[3]
        store = await self.service.update(
            store_id=self.store.id,
            user=self.user,
            store_name="New Name",
            store_type=store_type_label,
            store_description="New Description",
        )
        self.assertEqual(store.name, "New Name")
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, "New Description")
        self.assertEqual(await store.auser(), self.user)

    async def test_update_store_does_not_exist(self) -> None:
        """Test updating non-existent store."""
        with self.assertRaises(StoreDoesNotExist):
            await self.service.update(
                store_id=99999999999,
                user=self.user,
                store_name="New Name",
            )

    async def test_update_store_invalid_type(self) -> None:
        """Test updating store with invalid type."""
        with self.assertRaises(InvalidStoreType):
            await self.service.update(
                store_id=self.store.id,
                user=self.user,
                store_type="Invalid Type",
            )

    async def test_update_store_name_already_exists(self) -> None:
        """Test updating store with name that already exists."""
        # Create another store with a different name
        other_store = await self.create(user=self.user, name="Other Store")

        with self.assertRaises(StoreAlreadyExists):
            await self.service.update(
                store_id=self.store.id,
                user=self.user,
                store_name=other_store.name,
            )
