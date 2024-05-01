"""Contains tests for api store service."""

from django.contrib.auth.models import User
from django.test import TestCase

from stores.models import ShoppingStore as Store
from stores.services import store_service

TEST_STORE = "Test Store"
TEST_STORE_TYPE = 1
TEST_DESCRIPTION = "Test Description"


class TestStoreServiceGetStores(TestCase):
    """Test the get stores function."""

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

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_get_stores(self) -> None:
        """Test the get stores function."""
        result = await store_service.get_stores()
        self.assertEqual(len(result.stores), 2)

        store_one_json = result.stores[0].model_dump()
        self.assertEqual(store_one_json["name"], "Alt Store")
        self.assertEqual(store_one_json["store_type"], 3)
        self.assertEqual(store_one_json["description"], "Alt Description")
        self.assertEqual(store_one_json["user"]["username"], "altuser")

        store_two_json = result.stores[1].model_dump()
        self.assertEqual(store_two_json["name"], TEST_STORE)
        self.assertEqual(store_two_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(store_two_json["description"], TEST_DESCRIPTION)
        self.assertEqual(store_two_json["user"]["username"], "testuser")

    async def test_get_stores_with_pagination(self) -> None:
        """Test the get stores function with pagination."""
        result = await store_service.get_stores(limit=1, page_number=1)
        self.assertEqual(len(result.stores), 1)
        self.assertEqual(result.total, 2)
        self.assertEqual(result.page_number, 1)
        self.assertEqual(result.total_pages, 2)
        self.assertEqual(result.has_previous, False)
        self.assertEqual(result.previous_page, None)
        self.assertEqual(result.has_next, True)
        self.assertEqual(result.next_page, 2)

        result = await store_service.get_stores(limit=1, page_number=2)
        self.assertEqual(len(result.stores), 1)
        self.assertEqual(result.total, 2)
        self.assertEqual(result.page_number, 2)
        self.assertEqual(result.total_pages, 2)
        self.assertEqual(result.has_previous, True)
        self.assertEqual(result.previous_page, 1)
        self.assertEqual(result.has_next, False)
        self.assertEqual(result.next_page, None)

    async def test_get_stores_for_user(self) -> None:
        """Test retrieving stores for a user."""
        result = await store_service.get_stores(user=self.user)
        self.assertEqual(len(result.stores), 1)

        store_one_json = result.stores[0].model_dump()
        self.assertEqual(store_one_json["name"], TEST_STORE)
        self.assertEqual(store_one_json["store_type"], TEST_STORE_TYPE)
        self.assertEqual(store_one_json["description"], TEST_DESCRIPTION)
        self.assertEqual(store_one_json["user"]["username"], "testuser")
