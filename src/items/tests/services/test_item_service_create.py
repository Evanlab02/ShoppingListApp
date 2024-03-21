"""Contains tests for the item service create function."""

import pytest
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.errors.exceptions import ItemAlreadyExists
from items.models import ShoppingItem as Item
from items.schemas.output import ItemSchema
from items.services import item_service
from stores.errors.api_exceptions import StoreDoesNotExist
from stores.models import ShoppingStore as Store

MOCK_NAME = "Logitech MX Keys Mini"
MOCK_DESRIPTION = "A mini keyboard created by logitech."


class TestItemServiceCreate(TestCase):
    """Test the item service create."""

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
        Item.objects.all().delete()
        return super().tearDown()

    async def test_create_item_type(self) -> None:
        """Test that the create item function returns the correct type."""
        item = await item_service.create_item(
            user=self.user,
            store_id=self.store.id,
            name=MOCK_NAME,
            price=2500,
            description=MOCK_DESRIPTION,
        )
        self.assertIsInstance(item, ItemSchema)

    async def test_create_item(self) -> None:
        """Test the create item function."""
        item = await item_service.create_item(
            user=self.user,
            store_id=self.store.id,
            name=MOCK_NAME,
            price=2500,
            description=MOCK_DESRIPTION,
        )

        item_dict = item.model_dump()
        user: dict[str, str] = item_dict.get("user", {})
        username = user.get("username", "")

        store: dict[str, str | int | float] = item_dict.get("store", {})
        store_name = store.get("name", "")
        store_type = store.get("store_type", 0)
        store_description = store.get("description", "")

        item_description = item_dict.get("description", "")
        item_name = item_dict.get("name", "")
        item_price = item_dict.get("price", "")

        self.assertEqual(username, self.user.username)

        self.assertEqual(store_name, "Base Test Store")
        self.assertEqual(store_type, 3)
        self.assertEqual(store_description, "")

        self.assertEqual(item_description, MOCK_DESRIPTION)
        self.assertEqual(item_name, MOCK_NAME)
        self.assertEqual(item_price, 2500)

    async def test_create_item_raises_error_with_invalid_store_id(self) -> None:
        """Test the create item function with invalid store id."""
        with pytest.raises(StoreDoesNotExist):
            await item_service.create_item(
                user=self.user,
                store_id=99999,
                name=MOCK_NAME,
                price=2500,
                description=MOCK_DESRIPTION,
            )

    async def test_create_item_raises_error_when_duplicating(self) -> None:
        """Test the create item function with duplicated entry."""
        await item_service.create_item(
            user=self.user,
            store_id=self.store.id,
            name=MOCK_NAME,
            price=2500,
            description=MOCK_DESRIPTION,
        )

        with pytest.raises(ItemAlreadyExists):
            await item_service.create_item(
                user=self.user,
                store_id=self.store.id,
                name=MOCK_NAME,
                price=2500,
                description=MOCK_DESRIPTION,
            )
