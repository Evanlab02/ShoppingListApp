"""Contains tests for api store service."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.errors.api_exceptions import StoreDoesNotExist
from stores.models import ShoppingStore as Store
from stores.services.store_service import get_store_detail, get_store_detail_with_items

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test Description"


class TestStoreService(TestCase):
    """Test the store service."""

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
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_get_store_detail(self) -> None:
        """Test the get store detail service function."""
        result = await get_store_detail(self.store.id)
        result_json = result.model_dump()
        self.assertEqual(result_json.get("id"), self.store.id)
        self.assertEqual(result_json.get("name"), self.store.name)
        self.assertEqual(result_json.get("store_type"), self.store.store_type)
        self.assertEqual(result_json.get("description"), self.store.description)
        self.assertIsNotNone(result_json.get("created_at"))
        self.assertIsNotNone(result_json.get("updated_at"))

    async def test_get_store_detail_invalid_id(self) -> None:
        """Test the get store detail service function with an invalid id."""
        with pytest.raises(StoreDoesNotExist):
            await get_store_detail(1000)

    async def test_get_store_detail_with_items(self) -> None:
        """Test the get store detail service function with items."""
        result, items = await get_store_detail_with_items(self.store.id)
        result_json = result.model_dump()
        self.assertEqual(result_json.get("id"), self.store.id)
        self.assertEqual(result_json.get("name"), self.store.name)
        self.assertEqual(result_json.get("store_type"), self.store.store_type)
        self.assertEqual(result_json.get("description"), self.store.description)
        self.assertIsNotNone(result_json.get("created_at"))
        self.assertIsNotNone(result_json.get("updated_at"))

        items_json = items.model_dump()
        self.assertEqual(items_json.get("total"), 0)
        self.assertEqual(items_json.get("page_number"), 1)
        self.assertEqual(items_json.get("total_pages"), 1)
        self.assertEqual(items_json.get("has_previous"), False)
        self.assertEqual(items_json.get("previous_page"), None)
        self.assertEqual(items_json.get("has_next"), False)
        self.assertEqual(items_json.get("next_page"), None)

    async def test_get_store_detail_with_items_with_invalid_id(self) -> None:
        """Test the get store detail service function with items."""
        with pytest.raises(StoreDoesNotExist):
            await get_store_detail_with_items(999999)
