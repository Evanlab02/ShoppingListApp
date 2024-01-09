"""Contains tests for the store repository functions."""


from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import filter_stores
from stores.models import ShoppingStore
from stores.schemas.output import StorePaginationSchema, StoreSchema

TEST_STORE = "Test User Store"
TEST_DESCRIPTION = "This is a test store."


class TestStoreRepoFilter(TestCase):
    """Store repository tests."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.base_user = User.objects.create(
            username="baseuser",
            email="baseuser@gmail.com",
            password="basepass",
            first_name="Base",
            last_name="User",
        )
        self.base_user.save()

        self.user = User.objects.create(
            username="testuser",
            email="testuser@gmail.com",
            password="testpass",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        self.base_store = ShoppingStore.objects.create(
            name="Base Test Store",
            store_type=3,
            description=TEST_DESCRIPTION,
            user=self.base_user,
        )
        self.base_store.save()

        name = TEST_STORE
        store_type = 1
        description = TEST_DESCRIPTION
        self.store = ShoppingStore.objects.create(
            name=name,
            store_type=store_type,
            description=description,
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

    async def base_check(self, paginated_data: StorePaginationSchema) -> None:
        """Check the base case."""
        self.assertIsInstance(paginated_data, StorePaginationSchema)

        stores = paginated_data.stores
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)

        store = stores[0]
        self.assertIsInstance(store, StoreSchema)
        self.assertEqual(store.name, self.store.name)
        self.assertEqual(store.store_type, self.store.store_type)
        self.assertEqual(store.description, self.store.description)

    async def test_filter_stores(self) -> None:
        """Test filter_stores."""
        paginated_data = await filter_stores()
        self.assertIsInstance(paginated_data, StorePaginationSchema)

        stores = paginated_data.stores
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 2)

    async def test_filter_stores_page_2_with_limit(self) -> None:
        """Test filter_stores with page and limit."""
        paginated_data = await filter_stores(page_number=2, stores_per_page=1)
        stores = paginated_data.stores
        page_number = paginated_data.page_number
        self.assertEqual(page_number, 2)
        self.assertIsInstance(stores, list)
        self.assertEqual(len(stores), 1)

    async def test_filter_stores_by_name(self) -> None:
        """Test filter_stores by name."""
        paginated_data = await filter_stores(name=self.store.name)
        await self.base_check(paginated_data)

    async def test_filter_stores_by_store_type(self) -> None:
        """Test filter_stores by store_type."""
        paginated_data = await filter_stores(store_types=[1])
        await self.base_check(paginated_data)

    async def test_filter_stores_by_created_on_date(self) -> None:
        """Test filter_stores by created_on_date."""
        self.store.created_at = datetime(2021, 1, 1, tzinfo=self.store.created_at.tzinfo)
        await self.store.asave()

        paginated_data = await filter_stores(created_on=self.store.created_at.date())
        await self.base_check(paginated_data)

    async def test_filter_stores_by_created_before_date(self) -> None:
        """Test filter_stores by created_before_date."""
        self.store.created_at = datetime(2021, 1, 1, tzinfo=self.store.created_at.tzinfo)
        await self.store.asave()

        paginated_data = await filter_stores(
            created_before=self.store.created_at.date() + timedelta(days=1)
        )
        await self.base_check(paginated_data)

    async def test_filter_stores_by_created_after_date(self) -> None:
        """Test filter_stores by created_after_date."""
        self.store.created_at = datetime(2021, 10, 1, tzinfo=self.store.created_at.tzinfo)
        await self.store.asave()

        self.base_store.created_at = datetime(2021, 1, 1, tzinfo=self.base_store.created_at.tzinfo)
        await self.base_store.asave()

        paginated_data = await filter_stores(
            created_before=self.store.created_at.date() + timedelta(days=1),
            created_after=self.store.created_at.date() - timedelta(days=5),
        )
        await self.base_check(paginated_data)

    async def test_filter_stores_by_user(self) -> None:
        """Test filter_stores by user."""
        paginated_data = await filter_stores(user=self.user)
        await self.base_check(paginated_data)
