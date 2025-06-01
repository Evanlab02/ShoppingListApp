"""Contains tests for the update_item function of the item repository."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.test.testcases import TestCase

from authentication.tests.factory import UserFactory
from items.database.item_repo import ItemRepo
from items.models import ShoppingItem as Item
from items.tests.factory import ItemFactory
from stores.models import ShoppingStore as Store
from stores.tests.factory import StoreFactory


class TestItemRepositoryUpdate(TestCase):
    """Test the item repository update_item function."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = UserFactory.create()
        self.store = StoreFactory.create(user=self.user)
        self.repo = ItemRepo()
        self.item = ItemFactory.create(
            user=self.user,
            store=self.store,
            name="Original Name",
            description="Original Description",
            price=10.0,
        )
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        Store.objects.all().delete()
        Item.objects.all().delete()
        User.objects.all().delete()
        return super().tearDown()

    async def test_update_item_name(self) -> None:
        """Test updating an item's name."""
        new_name = "Updated Name"
        updated_item = await self.repo.update_item(self.item, name=new_name)

        self.assertEqual(updated_item.name, new_name)
        self.assertEqual(updated_item.description, self.item.description)
        self.assertEqual(updated_item.price, self.item.price)
        self.assertEqual(updated_item.store, self.store)

        await self.item.arefresh_from_db()
        self.assertEqual(self.item.name, new_name)

    async def test_update_item_description(self) -> None:
        """Test updating an item's description."""
        new_description = "Updated Description"
        updated_item = await self.repo.update_item(self.item, description=new_description)

        self.assertEqual(updated_item.name, self.item.name)
        self.assertEqual(updated_item.description, new_description)
        self.assertEqual(updated_item.price, self.item.price)
        self.assertEqual(updated_item.store, self.store)

        await self.item.arefresh_from_db()
        self.assertEqual(self.item.description, new_description)

    async def test_update_item_price(self) -> None:
        """Test updating an item's price."""
        new_price = 20.0
        updated_item = await self.repo.update_item(self.item, price=new_price)

        self.assertEqual(updated_item.name, self.item.name)
        self.assertEqual(updated_item.description, self.item.description)
        self.assertEqual(updated_item.price, new_price)
        self.assertEqual(updated_item.store, self.store)

        await self.item.arefresh_from_db()
        self.assertEqual(self.item.price, new_price)

    async def test_update_item_store(self) -> None:
        """Test updating an item's store."""
        new_store = await sync_to_async(StoreFactory.create)(user=self.user)
        updated_item = await self.repo.update_item(self.item, store=new_store.id)

        await updated_item.arefresh_from_db()
        self.assertEqual(updated_item.name, self.item.name)
        self.assertEqual(updated_item.description, self.item.description)
        self.assertEqual(updated_item.price, self.item.price)
        self.assertEqual(await updated_item.astore(), new_store)

        await self.item.arefresh_from_db()
        self.assertEqual(await self.item.astore(), new_store)

    async def test_update_item_multiple_fields(self) -> None:
        """Test updating multiple fields of an item at once."""
        new_name = "Updated Name"
        new_description = "Updated Description"
        new_price = 20.0
        new_store = await sync_to_async(StoreFactory.create)(user=self.user)

        updated_item = await self.repo.update_item(
            self.item,
            name=new_name,
            description=new_description,
            price=new_price,
            store=new_store.id,
        )

        await updated_item.arefresh_from_db()
        self.assertEqual(updated_item.name, new_name)
        self.assertEqual(updated_item.description, new_description)
        self.assertEqual(updated_item.price, new_price)
        self.assertEqual(await updated_item.astore(), new_store)

        await self.item.arefresh_from_db()
        self.assertEqual(self.item.name, new_name)
        self.assertEqual(self.item.description, new_description)
        self.assertEqual(self.item.price, new_price)
        self.assertEqual(await self.item.astore(), new_store)
