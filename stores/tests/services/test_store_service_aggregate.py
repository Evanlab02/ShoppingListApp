"""Contains tests for api store service."""

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.models import ShoppingStore as Store
from stores.services import store_service

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test Description"


class TestAggregate(TestCase):
    @pytest.mark.django_db(transaction=True)
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
        self.alt_store = Store.objects.create(
            name="Alt Store",
            store_type=3,
            description="Alt Description",
            user=self.alt_user,
        )
        self.alt_store.save()
        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_store_aggregation(self) -> None:
        """Test the store aggregation function."""
        result = await store_service.aggregate()
        result_json = result.model_dump()

        self.assertEqual(result_json.get("total_stores"), 2)
        self.assertEqual(result_json.get("online_stores"), 1)
        self.assertEqual(result_json.get("in_store_stores"), 0)
        self.assertEqual(result_json.get("combined_stores"), 1)
        self.assertEqual(result_json.get("combined_online_stores"), 2)
        self.assertEqual(result_json.get("combined_in_store_stores"), 1)
