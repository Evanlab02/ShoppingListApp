"""Contains the interfaces for the item repository."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.schemas.output import ItemPaginationSchema


class IItemRepo(ABC):
    """Interface for the item repository."""

    def __init__(self) -> None:
        """Initialize the item repository."""
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
        Create a shopping item.

        Args:
            user (User): The user that created the item.
            store_id (int): The store where the item is stocked.
            name (str): The item name.
            price (float): The price of the item.
            description (str): The item description.

        Returns:
            Item: The created item.
        """

    @abstractmethod
    async def get_items(
        self,
        page: int = 1,
        items_per_page: int = 10,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
        store: int | None = None,
        name: str | None = None,
        search: ItemSearchSchema | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> ItemPaginationSchema:
        """
        Get all the items.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            user (User): The user to filter off.
            store (int): Specific store to filter off.
            name (int): The full or partial name of the item to filter by.
            search (ItemSearchSchema): The search object for advanced filtering/searching.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            ItemPaginationSchema: The paginated items.
        """

    @abstractmethod
    async def get_item(self, item_id: int) -> Item:
        """
        Get an item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Item: The item.
        """

    @abstractmethod
    async def get_item_for_user(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> Item:
        """
        Get an item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Item: The item.
        """

    @abstractmethod
    async def update_item(
        self,
        item: Item,
        name: str | None = None,
        price: float | None = None,
        description: str | None = None,
        store: int | None = None,
    ) -> Item:
        """
        Update an item.

        Args:
            item (Item): The item to update.
            name (str | None): The new name of the item.
            price (float | None): The new price of the item.
            description (str | None): The new description of the item.
            store (int | None): The new store for the item.

        Returns:
            Item: The updated item.
        """

    @abstractmethod
    async def delete_item(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> None:
        """
        Delete an item by its ID.

        Args:
            item_id (int): The ID of the item.
            user (User | AnonymousUser | AbstractBaseUser): The user who created the item.

        Raises:
            Item.DoesNotExist: If the item does not exist.
        """

    @abstractmethod
    async def aggregate(
        self,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
    ) -> dict[str, Any]:
        """
        Aggregate the items.

        Returns:
            dict[str, Any]: The aggregation of the items.
        """

    @abstractmethod
    async def does_item_exist(
        self,
        name: str,
        store_id: int | None = None,
    ) -> bool:
        """
        Check if a item exists with the provided details.

        Args:
            name (str): The name of the item.
            store_id (int): The store we are checking against.

        Returns:
            bool: True if the item exists, false otherwise.
        """
