"""Contains the tests for the store create service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from stores.errors.exceptions import InvalidStoreType, StoreAlreadyExists
from stores.schemas.input import NewStore
from stores.services.store_service import StoreService


class TestStoreCreate(TestCase):
    """Test the store create service."""

    def setUp(self) -> None:
        """Set up the test."""
        self.service = StoreService()
        self.user = UserFactory.create()
        super().setUp()

    async def test_store_create_success(self) -> None:
        """Test the store create service."""
        new_store = NewStore(
            name="Test Store",
            store_type=3,
            description="Test Description",
        )
        store = await self.service.create(new_store, self.user)

        self.assertEqual(store.name, "Test Store")
        self.assertEqual(store.store_type, 3)
        self.assertEqual(store.description, "Test Description")
        self.assertEqual(store.user, self.user)

    async def test_store_type_str_conversion(self) -> None:
        """Test the store type str conversion."""
        new_store = NewStore(
            name="Test Store",
            store_type="Online",
            description="Test Description",
        )
        store = await self.service.create(new_store, self.user)

        self.assertEqual(store.name, "Test Store")
        self.assertEqual(store.store_type, 1)
        self.assertEqual(store.description, "Test Description")
        self.assertEqual(store.user, self.user)

    async def test_store_type_invalid_int(self) -> None:
        """Test the store type invalid int."""
        new_store = NewStore(
            name="Test Store",
            store_type=10,
            description="Test Description",
        )

        with self.assertRaises(InvalidStoreType):
            await self.service.create(new_store, self.user)

    async def test_store_type_invalid_str(self) -> None:
        """Test the store type invalid str."""
        new_store = NewStore(
            name="Test Store",
            store_type="Invalid",
            description="Test Description",
        )

        with self.assertRaises(InvalidStoreType):
            await self.service.create(new_store, self.user)

    async def test_store_name_already_exists(self) -> None:
        """Test the store name already exists."""
        new_store = NewStore(
            name="Test Store",
            store_type=3,
            description="Test Description",
        )
        await self.service.create(new_store, self.user)

        with self.assertRaises(StoreAlreadyExists):
            await self.service.create(new_store, self.user)
