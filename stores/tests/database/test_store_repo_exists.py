"""Contains tests for database store repo."""

from django.contrib.auth.models import User
from django.test import TestCase

from stores.database.store_repo import does_name_exist
from stores.models import ShoppingStore as Store


class TestStoreRepo(TestCase):
    """Contains tests for database store repo."""

    def setUp(self) -> None:
        """Set up the tests."""
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@gmail.com",
            password="testing123",
        )
        self.user.save()

        self.store = Store.objects.create(
            name="Test Store",
            store_type=1,
            description="Test Description",
            user=self.user,
        )
        self.store.save()
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the tests."""
        User.objects.all().delete()
        Store.objects.all().delete()
        return super().tearDown()

    async def test_store_exists(self) -> None:
        """Test store exists."""
        store_exists = await does_name_exist("Test Store")
        self.assertTrue(store_exists)

    async def test_store_does_not_exist(self) -> None:
        """Test store does not exist."""
        store_exists = await does_name_exist("Does Not Exist")
        self.assertFalse(store_exists)
