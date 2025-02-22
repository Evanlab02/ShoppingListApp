"""Contains interfaces for the item services."""

import logging
from abc import ABC, abstractmethod
from typing import Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema
from shoppingapp.schemas.shared import DeleteSchema


class IItemService(ABC):
    """Interface for the item services."""

    def __init__(self) -> None:
        """Initialize the item service."""
        self.log = logging.getLogger(__name__)

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    async def get_item_detail(self, item_id: int) -> Item:
        """
        Get an item using the item id.

        Args:
            item_id (int): The item id.

        Returns:
            ItemSchema: The item detail.
        """

    @abstractmethod
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
            ItemSchema: The item details.

        Raises:
            ItemDoesNotExist: If the item id provided does not exist.
            ItemAlreadyExists: If you are attempting to create a duplicate item at the given store.
            StoreDoesNotExist: If the store id provided is invalid.
        """

    @abstractmethod
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

    @abstractmethod
    async def aggregate(
        self,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
    ) -> ItemAggregationSchema:
        """
        Aggregate the items.

        Args:
            user (User): The user to filter off.

        Returns:
            ItemAggregationSchema: The aggregation of the items.
        """
