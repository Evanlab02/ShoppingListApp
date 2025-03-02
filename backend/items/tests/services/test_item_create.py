"""Contains tests for the item create service."""

from django.test import TestCase

from authentication.tests.factory import UserFactory
from items.errors.exceptions import ItemAlreadyExists
from items.services.item_service import ItemService
from items.tests.factory import ItemFactory
from stores.errors.api_exceptions import StoreDoesNotExist
from stores.tests.factory import StoreFactory


class TestItemCreateService(TestCase):
    """Tests for the item create service."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.item_service = ItemService()
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.item = ItemFactory.create(store=self.store, user=self.user)

    async def test_create_item(self) -> None:
        """Test the create item method."""
        item = await self.item_service.create_item(
            store_id=self.store.id,
            user=self.user,
            name="Test Item",
            price=100.00,
            description="Test Description",
        )
        store = await item.astore()
        user = await item.auser()
        self.assertEqual(item.name, "Test Item")
        self.assertEqual(item.price, 100.00)
        self.assertEqual(item.description, "Test Description")
        self.assertEqual(store.id, self.store.id)
        self.assertEqual(user.id, self.user.id)

    async def test_create_item_that_already_exists(self) -> None:
        """Test the create item method when the item already exists."""
        with self.assertRaises(ItemAlreadyExists):
            await self.item_service.create_item(
                store_id=self.store.id,
                user=self.user,
                name=self.item.name,
                price=float(self.item.price),
                description=self.item.description,
            )

    async def test_create_item_with_invalid_store_id(self) -> None:
        """Test the create item method with an invalid store id."""
        with self.assertRaises(StoreDoesNotExist):
            await self.item_service.create_item(
                store_id=99999,
                user=self.user,
                name="Test Item",
                price=100.00,
                description="Test Description",
            )
