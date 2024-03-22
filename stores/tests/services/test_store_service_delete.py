"""Contains tests for api store service."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.errors.api_exceptions import StoreDoesNotExist
from stores.models import ShoppingStore as Store
from stores.services import store_service

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test Description"


class TestAggregate(TestCase):
    """Test the store aggregation function."""

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
        self.alt_user = User.objects.create_user(
            username="altuser",
            email="altuser@gmail.com",
            password="testing123",
        )
        self.alt_user.save()
        return super().setUp()

    async def test_delete_one(self) -> None:
        """Delete store works as expected."""
        response = await store_service.delete_store(self.store.id, self.user)
        number_of_stores = await Store.objects.acount()
        self.assertEqual(number_of_stores, 0)

        result = response.model_dump()
        self.assertEqual(result.get("message"), "Deleted Store.")
        self.assertEqual(result.get("detail"), f"Store with ID #{self.store.id} was deleted.")

    async def test_delete_one_with_invalid_id_raises_correct_error(self) -> None:
        """Delete store raises correct error with invalid id."""
        with pytest.raises(StoreDoesNotExist):
            await store_service.delete_store(99999, self.user)

    async def test_delete_store_raises_error_if_owner_does_not_own_store(self) -> None:
        """Delete store raises correct error with invalid owner."""
        with pytest.raises(StoreDoesNotExist):
            await store_service.delete_store(self.store.id, self.alt_user)
