"""Contains tests for the get stores endpoint."""

from django.contrib.auth.models import User
from django.test import Client, TestCase

from stores.models import ShoppingStore as Store

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test description"


class TestGetStores(TestCase):
    """Test the get stores endpoint."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.client = Client()
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

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    def test_get_stores(self) -> None:
        """Test the get stores endpoint."""
        result = self.client.get("/api/v1/stores")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total"], 2)
        self.assertEqual(len(result_json["stores"]), 2)
        self.assertEqual(result_json["stores"][1]["name"], TEST_STORE)
        self.assertEqual(result_json["stores"][1]["store_type"], TEST_STORE_TYPE)
        self.assertEqual(result_json["stores"][1]["description"], TEST_DESCRIPTION)
        self.assertEqual(result_json["stores"][1]["user"]["username"], self.user.username)
        self.assertEqual(result_json["stores"][0]["name"], self.alt_store.name)
        self.assertEqual(result_json["stores"][0]["store_type"], self.alt_store.store_type)
        self.assertEqual(result_json["stores"][0]["description"], self.alt_store.description)
        self.assertEqual(result_json["stores"][0]["user"]["username"], self.alt_user.username)

    def test_get_stores_paginated(self) -> None:
        """Test the get stores endpoint with pagination."""
        result = self.client.get("/api/v1/stores?limit=1&offset=0")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total"], 2)
        self.assertEqual(len(result_json["stores"]), 1)
        self.assertEqual(result_json["stores"][0]["name"], self.alt_store.name)
        self.assertEqual(result_json["stores"][0]["store_type"], self.alt_store.store_type)
        self.assertEqual(result_json["stores"][0]["description"], self.alt_store.description)
        self.assertEqual(result_json["stores"][0]["user"]["username"], self.alt_user.username)

        result = self.client.get("/api/v1/stores?limit=1&offset=1")
        self.assertEqual(result.status_code, 200)

        result_json = result.json()
        self.assertEqual(result_json["total"], 2)
        self.assertEqual(len(result_json["stores"]), 1)
        self.assertEqual(result_json["stores"][0]["name"], TEST_STORE)
        self.assertEqual(result_json["stores"][0]["store_type"], TEST_STORE_TYPE)
        self.assertEqual(result_json["stores"][0]["description"], TEST_DESCRIPTION)
        self.assertEqual(result_json["stores"][0]["user"]["username"], self.user.username)
