"""Contains the item service."""

from typing import Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.database.interfaces.i_item_repo import IItemRepo
from items.database.item_repo import ItemRepo
from items.errors.exceptions import ItemAlreadyExists, ItemDoesNotExist
from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema
from items.services.interfaces.i_item_service import IItemService
from shoppingapp.schemas.shared import DeleteSchema
from stores.database.interfaces.i_store_repo import IStoreRepo
from stores.database.store_repo import StoreRepo
from stores.errors.api_exceptions import StoreDoesNotExist


class ItemService(IItemService):
    """Item service."""

    def __init__(
        self,
        item_repo: IItemRepo = ItemRepo(),
        store_repo: IStoreRepo = StoreRepo(),
    ) -> None:
        """Initialize the item service."""
        self.repo = item_repo
        self.store_repo = store_repo
        super().__init__()

    async def create_item(
        self,
        user: User | AbstractBaseUser | AnonymousUser,
        store_id: int,
        name: str,
        price: float,
        description: str = "",
    ) -> Item:
        """
        Create an item.

        Args:
            user (User): The user that created the item.
            store (int): The store id that the item belongs to.
            name (str): The new item name.
            price (float): The price of the item.
            description (str): The description of the item.

        Returns:
            ItemSchema: The item that was created.

        Raises:
            ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
        """
        if await self.repo.does_item_exist(name=name, store_id=store_id):
            raise ItemAlreadyExists(item_name=name, store_name=str(store_id))
        if not await self.store_repo.does_store_exist(store_id=store_id):
            raise StoreDoesNotExist(store_id=store_id)

        return await self.repo.create_item(
            user=user,
            store_id=store_id,
            name=name,
            price=price,
            description=description,
        )

    async def get_items(
        self,
        page: int = 1,
        items_per_page: int = 10,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
        store: int | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> ItemPaginationSchema:
        """
        Get all items.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            user (User): The user to filter off.
            store (int): Specific store to filter off.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            ItemPaginationSchema: A paginated list of items.
        """
        return await self.repo.get_items(
            page=page,
            items_per_page=items_per_page,
            user=user,
            store=store,
            sort=sort,
            sort_dir=sort_dir,
        )

    async def search_items(
        self,
        page: int = 1,
        limit: int = 10,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
        name: str | None = None,
        store_id: int | None = None,
        search: ItemSearchSchema | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> ItemPaginationSchema:
        """
        Search items based on the provided filters.

        Args:
            page (int): The page number.
            limit (int): The number of items per page.
            user (User): The user to filter off.
            name (int): The full or partial name of the item to filter by.
            store_id (int): Specific store to filter off.
            search (ItemSearchSchema): The search object for advanced filtering/searching.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            ItemPaginationSchema: Returns the item pagination schema.
        """
        return await self.repo.get_items(
            name=name,
            items_per_page=limit,
            page=page,
            store=store_id,
            user=user,
            search=search,
            sort=sort,
            sort_dir=sort_dir,
        )

    async def get_item_detail(self, item_id: int) -> Item:
        """
        Get an item using the item id.

        Args:
            item_id (int): The item id.

        Returns:
            ItemSchema: The item detail.

        Raises:
            ItemDoesNotExist: If the item id provided does not exist.
        """
        try:
            return await self.repo.get_item(item_id=item_id)
        except Item.DoesNotExist:
            self.log.warning(f"Item with ID: {item_id} does not exist.")
            raise ItemDoesNotExist(item_id=item_id)

    async def get_item_for_user(
        self, item_id: int, user: User | AbstractBaseUser | AnonymousUser
    ) -> Item:
        """
        Get an item for a user.

        Args:
            item_id (int): The item id.
            user (User): The user to filter off.

        Returns:
            ItemSchema: The item detail.
        """
        try:
            return await self.repo.get_item_for_user(item_id=item_id, user=user)
        except Item.DoesNotExist:
            self.log.warning(f"Item with ID: {item_id} does not exist for user: {user}.")
            raise ItemDoesNotExist(item_id=item_id)

    async def update_item(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
        new_name: str | None = None,
        new_price: float | None = None,
        new_description: str | None = None,
        new_store_id: int | None = None,
    ) -> Item:
        """
        Update an item using the item id.

        Args:
            item_id (int): The item id.
            user (User): The user that is updating the item.
            name (str): The new item name.
            price (float): The price of the item.
            description (str): The description of the item.
            store_id (int): The store id that the item belongs to.

        Returns:
            Item: The item details.

        Raises:
            ItemDoesNotExist: If the item id provided does not exist.
            ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
            StoreDoesNotExist: If the store id provided is invalid.
        """
        try:
            item = await self.repo.get_item_for_user(item_id=item_id, user=user)
            store = new_store_id if new_store_id else item.store.id
            name = new_name if new_name else item.name
            item_exists = await self.repo.does_item_exist(name=name, store_id=store)
            store_exists = await self.store_repo.does_store_exist(store_id=store)
        except Item.DoesNotExist:
            raise ItemDoesNotExist(item_id=item_id)

        store = new_store_id if new_store_id else item.store.id
        name = new_name if new_name else item.name

        item_exists = await self.repo.does_item_exist(name=name, store_id=store)
        if item_exists:
            raise ItemAlreadyExists(item_name=name, store_name=str(store))

        if not store_exists:
            raise StoreDoesNotExist(store_id=store)

        return await self.repo.update_item(
            item=item,
            name=name,
            price=new_price,
            description=new_description,
            store=store,
        )

    async def delete_item(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> DeleteSchema:
        """
        Delete an item using the item id.

        Args:
            item_id (int): The item id.
            user (User): The user that created the item.

        Returns:
            DeleteSchema: The deletion result.
        """
        try:
            await self.repo.delete_item(item_id=item_id, user=user)
            return DeleteSchema(
                message="Deleted Item.", detail=f"Item with ID #{item_id} was deleted."
            )
        except Item.DoesNotExist:
            self.log.warning(
                f"Item with ID: {item_id} does not exist for user: {user}. (For deletion)"
            )
            raise ItemDoesNotExist(item_id=item_id)

    async def aggregate(
        self,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
    ) -> ItemAggregationSchema:
        """
        Aggregate the items.

        Returns:
            ItemAggregationSchema: The aggregation of the items.
        """
        aggregation = await self.repo.aggregate(user=user)
        return ItemAggregationSchema.model_validate(aggregation)
