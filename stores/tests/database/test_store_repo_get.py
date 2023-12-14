"""Contains tests for the store repository functions."""


import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import get_stores
from stores.models import ShoppingStore, ShoppingStorePagination

TEST_STORE = "Test User Store"
TEST_DESCRIPTION = "This is a test store."


class TestStoreRepoCreate(TestCase):
    """Store repository tests."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        self.store = ShoppingStore.objects.create(
            name="Base Test Store",
            store_type=3,
            description=TEST_DESCRIPTION,
            user=self.user,
        )
        self.store.save()

        return super().setUp()

    @pytest.mark.django_db(transaction=True)
    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        ShoppingStore.objects.all().delete()
        return super().tearDown()

    async def test_get_stores(self) -> None:
        """Test get_stores."""
        paginated_data = await get_stores()

        self.assertIsInstance(paginated_data, ShoppingStorePagination)

        stores = paginated_data.stores
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)

        store = stores[0]
        self.assertIsInstance(store, ShoppingStore)
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, self.store.description)

    async def test_get_stores_page(self) -> None:
        """Test get_stores with page."""
        name = TEST_STORE
        store_type = 1
        description = TEST_DESCRIPTION
        store = await ShoppingStore.objects.acreate(
            name=name,
            store_type=store_type,
            description=description,
            user=self.user,
        )
        await store.asave()

        paginated_data = await get_stores(page_number=1)
        self.assertIsInstance(paginated_data, ShoppingStorePagination)

        stores = paginated_data.stores
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 2)

    async def test_get_stores_page_2(self) -> None:
        """Test get_stores with page."""
        paginated_data = await get_stores(page_number=2)
        stores = paginated_data.stores
        page_number = paginated_data.page_number
        self.assertEqual(page_number, 1)
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)

    async def test_get_stores_page_with_limit(self) -> None:
        """Test get_stores with page and limit."""
        name = TEST_STORE
        store_type = 1
        description = TEST_DESCRIPTION
        store = await ShoppingStore.objects.acreate(
            name=name,
            store_type=store_type,
            description=description,
            user=self.user,
        )
        await store.asave()

        paginated_data = await get_stores(page_number=1, stores_per_page=1)
        self.assertIsInstance(paginated_data, ShoppingStorePagination)

        stores = paginated_data.stores
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)

    async def test_get_stores_page_2_with_limit(self) -> None:
        """Test get_stores with page and limit."""
        name = TEST_STORE
        store_type = 1
        description = TEST_DESCRIPTION
        store = await ShoppingStore.objects.acreate(
            name=name,
            store_type=store_type,
            description=description,
            user=self.user,
        )
        await store.asave()

        paginated_data = await get_stores(page_number=2, stores_per_page=1)
        stores = paginated_data.stores
        page_number = paginated_data.page_number
        self.assertEqual(page_number, 2)
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)
