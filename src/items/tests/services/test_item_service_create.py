"""Contains tests for the item service create function."""

from django.contrib.auth.models import User
from django.test.testcases import TestCase

from items.schemas.output import ItemSchema
from items.services import item_service
from stores.models import ShoppingStore as Store


class TestStoreServiceCreate(TestCase):
    """Test the store service create."""

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

    async def test_create_item_type(self) -> None:
        """Test that the create item function returns the correct type."""
        item = await item_service.create_item(
            user=self.user,
            store=self.store,
        )
        self.assertIsInstance(item, ItemSchema)

    async def test_create_item(self) -> None:
        """Test the create item function."""
        # item = await item_service.create_item(
        #     user=self.user,
        #     store=self.store,
        #     name="Logitech MX Keys Mini",
        #     price=2500,
        #     description="A mini keyboard created by logitech.",
        # )

        item = await item_service.create_item(
            user=self.user,
            store=self.store,
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

        self.assertEqual(
            item_description, "Gaming headphones created for gamers designed by gamers."
        )
        self.assertEqual(item_name, "Logitech G Pro X")
        self.assertEqual(item_price, 2500)
