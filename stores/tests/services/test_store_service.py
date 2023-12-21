"""Contains tests for api store service."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.errors.api_exceptions import InvalidStoreType, StoreAlreadyExists
from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore
from stores.services.store_service import create

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test Description"


class TestStoreService(TestCase):
    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testing123",
        )
        self.user.save()
        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_create_store(self) -> None:
        """Test create store."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=TEST_STORE_TYPE,
            description=TEST_DESCRIPTION,
        )
        store = await create(new_store, self.user)
        store_dict = store.model_dump()
        self.assertEqual(store_dict.get("name"), TEST_STORE)
        self.assertEqual(store_dict.get("store_type"), TEST_STORE_TYPE)
        self.assertEqual(store_dict.get("description"), TEST_DESCRIPTION)
        self.assertIsInstance(store_dict.get("id"), int)

    async def test_create_store_invalid_store_type(self) -> None:
        """Test create store with invalid store type."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type="Invalid",
            description=TEST_DESCRIPTION,
        )
        with self.assertRaises(InvalidStoreType):
            await create(new_store, self.user)

    async def test_create_store_duplicate_name(self) -> None:
        """Test create store with duplicate name."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=TEST_STORE_TYPE,
            description=TEST_DESCRIPTION,
        )
        await create(new_store, self.user)
        with self.assertRaises(StoreAlreadyExists):
            await create(new_store, self.user)

    async def test_create_store_online_type_int(self) -> None:
        """Test create store with online type as int."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=1,
            description=TEST_DESCRIPTION,
        )
        store = await create(new_store, self.user)
        store_dict = store.model_dump()
        self.assertEqual(store_dict.get("name"), TEST_STORE)
        self.assertEqual(store_dict.get("store_type"), TEST_STORE_TYPE)
        self.assertEqual(store_dict.get("description"), TEST_DESCRIPTION)
        self.assertIsInstance(store_dict.get("id"), int)

    async def test_create_store_in_store_type_int(self) -> None:
        """Test create store with in store type as int."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=2,
            description=TEST_DESCRIPTION,
        )
        store = await create(new_store, self.user)
        store_dict = store.model_dump()
        self.assertEqual(store_dict.get("name"), TEST_STORE)
        self.assertEqual(store_dict.get("store_type"), 2)
        self.assertEqual(store_dict.get("description"), TEST_DESCRIPTION)
        self.assertIsInstance(store_dict.get("id"), int)

    async def test_create_store_both_type_int(self) -> None:
        """Test create store with both type as int."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=3,
            description=TEST_DESCRIPTION,
        )
        store = await create(new_store, self.user)
        store_dict = store.model_dump()
        self.assertEqual(store_dict.get("name"), TEST_STORE)
        self.assertEqual(store_dict.get("store_type"), 3)
        self.assertEqual(store_dict.get("description"), TEST_DESCRIPTION)
        self.assertIsInstance(store_dict.get("id"), int)

    async def test_create_store_invalid_store_type_int(self) -> None:
        """Test create store with invalid store type int."""
        new_store = NewStore(
            name=TEST_STORE,
            store_type=4,
            description=TEST_DESCRIPTION,
        )
        with self.assertRaises(InvalidStoreType):
            await create(new_store, self.user)
