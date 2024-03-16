"""Test the item router."""

from django.contrib.auth.models import User
from django.test import AsyncClient, TestCase

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

CREATE_ENDPOINT = "/api/v1/items/create"
CONTENT_TYPE = "application/json"
DUPLICATE_MOCK = "Duplicate Item"


class TestItemRouter(TestCase):
    """Test the item router."""

    def setUp(self) -> None:
        """Set up the test case."""
        self.client = AsyncClient()  # type: ignore
        self.user = User.objects.create_user(
            username="testuser",
            email="test@gmail.com",
            password="testpassword",
            first_name="Test",
            last_name="User",
        )
        self.user.save()

        self.store = Store.objects.create(
            name="Takealot",
            store_type=3,
            description="",
            user=self.user,
        )
        self.store.save()

        self.item = Item.objects.create(
            name=DUPLICATE_MOCK,
            description="",
            price=200,
            store=self.store,
            user=self.user,
        )
        self.item.save()

        self.client.force_login(self.user)
        return super().setUp()

    def tearDown(self) -> None:
        """Tear down the test case."""
        User.objects.all().delete()
        Store.objects.all().delete()
        Item.objects.all().delete()
        return super().tearDown()

    async def test_create_item(self) -> None:
        """Test creating a item."""
        response = await self.client.post(
            CREATE_ENDPOINT,
            {
                "store_id": self.store.id,
                "name": "Logitech G Pro X",
                "price": 2500,
                "description": "Headphones for gamers.",
            },
            content_type=CONTENT_TYPE,
        )  # type: ignore

        self.assertEqual(response.status_code, 201)

        response_json = response.json()
        user = response_json.get("user")
        username = user.get("username")
        self.assertEqual(username, self.user.username)

        store = response_json.get("store")
        store_name = store.get("name")
        self.assertEqual(store_name, "Takealot")

        name = response_json.get("name")
        description = response_json.get("description")
        price = response_json.get("price")

        self.assertEqual(name, "Logitech G Pro X")
        self.assertEqual(description, "Headphones for gamers.")
        self.assertEqual(price, "2500.0")

    async def test_create_item_default_description(self) -> None:
        """Test creating a item."""
        response = await self.client.post(
            CREATE_ENDPOINT,
            {
                "store_id": self.store.id,
                "name": "Default Description",
                "price": 100,
            },
            content_type=CONTENT_TYPE,
        )  # type: ignore

        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        description = response_json.get("description")
        self.assertEqual(description, "")

    async def test_create_item_duplicate(self) -> None:
        """Test creating a item."""
        response = await self.client.post(
            CREATE_ENDPOINT,
            {
                "store_id": self.store.id,
                "name": DUPLICATE_MOCK,
                "price": 200,
            },
            content_type=CONTENT_TYPE,
        )  # type: ignore

        self.assertEqual(response.status_code, 400)

    async def test_create_item_store_does_not_exist(self) -> None:
        """Test creating a item."""
        response = await self.client.post(
            CREATE_ENDPOINT,
            {
                "store_id": 99999,
                "name": "Test Item",
                "price": 200,
            },
            content_type=CONTENT_TYPE,
        )  # type: ignore

        self.assertEqual(response.status_code, 404)
