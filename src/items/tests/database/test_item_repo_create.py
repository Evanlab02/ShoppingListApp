"""Contains tests for the create function of the item repository."""

from datetime import datetime

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.database import item_repo
from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

MOCK_NAME = "Test Item"
MOCK_DESRIPTION = "Test Description"


class TestItemRepositoryCreate(TestCase):
    """Test the item repository create function."""

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

        self.store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_create_type(self) -> None:
        """Test the create function returns the correct type."""
        item = await item_repo.create_item(
            user=self.user,
            store=self.store,
            name=MOCK_NAME,
            price=100,
        )
        self.assertIsInstance(item, Item)

    async def test_create(self) -> None:
        """Test that the create function creates correctly."""
        item = await item_repo.create_item(
            user=self.user,
            store=self.store,
            name=MOCK_NAME,
            price=100.50,
            description=MOCK_DESRIPTION,
        )

        self.assertEqual(item.user, self.user)
        self.assertEqual(item.store, self.store)
        self.assertEqual(item.name, MOCK_NAME)
        self.assertEqual(item.price, 100.50)
        self.assertEqual(item.description, MOCK_DESRIPTION)
        self.assertIsInstance(item.created_at, datetime)
        self.assertIsInstance(item.updated_at, datetime)

    async def test_create_description_default(self) -> None:
        """Test that the create function uses the correct default if description is empty."""
        item = await item_repo.create_item(
            user=self.user,
            store=self.store,
            name=MOCK_NAME,
            price=100.50,
        )

        self.assertEqual(item.description, "")

    async def test_create_number_of_items_is_correct(self) -> None:
        """Test that when creating items the count in the db is correct."""
        item_count = await Item.objects.acount()
        self.assertEqual(item_count, 0)

        await item_repo.create_item(
            user=self.user,
            store=self.store,
            name=MOCK_NAME,
            price=100.50,
        )

        item_count = await Item.objects.acount()
        self.assertEqual(item_count, 1)

    async def test_create_query_from_models_is_correct(self) -> None:
        """Test that the create function creates correctly."""
        created_item = await item_repo.create_item(
            user=self.user,
            store=self.store,
            name=MOCK_NAME,
            price=100.50,
            description=MOCK_DESRIPTION,
        )

        item = await Item.objects.aget(id=created_item.id)

        self.assertEqual(item.name, MOCK_NAME)
        self.assertEqual(item.price, 100.50)
        self.assertEqual(item.description, MOCK_DESRIPTION)
        self.assertIsInstance(item.created_at, datetime)
        self.assertIsInstance(item.updated_at, datetime)
