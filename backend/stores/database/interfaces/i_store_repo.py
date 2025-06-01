"""Contains interfaces for the store repositories."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore as Store
from stores.schemas.input import StoreSearch
from stores.schemas.output import StorePaginationSchema


class IStoreRepo(ABC):
    """Interface for the store repository."""

    def __init__(self) -> None:
        """Initialize the store repository."""
        self.log = logging.getLogger(__name__)
        super().__init__()

    @abstractmethod
    async def create_store(
        self,
        name: str,
        store_type: int,
        description: str,
        user: User | AnonymousUser | AbstractBaseUser,
    ) -> Store:
        """
        Create a store.

        Args:
            name (str): The name of the store.
            store_type (int): The type of the store.
            description (str): The description of the store.
            user (User | AnonymousUser | AbstractBaseUser): The user who created the store.

        Returns:
            ShoppingStore: The created store.
        """

    @abstractmethod
    async def get_stores(
        self,
        page_number: int = 1,
        stores_per_page: int = 10,
        user: User | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Get all stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            StorePaginationSchema: The paginated stores.
        """

    @abstractmethod
    async def search_stores(
        self,
        page_number: int = 1,
        stores_per_page: int = 10,
        name: str | None = None,
        user: User | None = None,
        search: StoreSearch | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Search for stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            name (str | None): The name of the store.
            user (User | None): The user who created the store.
            search (StoreSearch | None): The search object containing the search parameters.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            StorePaginationSchema: The paginated stores.
        """

    @abstractmethod
    async def get_store(self, store_id: int) -> Store:
        """
        Get a store.

        Args:
            store_id (int): The id of the store.

        Returns:
            ShoppingStore: The store.

        Raises:
            Store.DoesNotExist: If the store does not exist.
        """

    @abstractmethod
    async def update_store(
        self,
        store_id: int,
        user: User | AnonymousUser | AbstractBaseUser,
        store_name: str | None = None,
        store_type: int | None = None,
        store_description: str | None = None,
    ) -> Store:
        """
        Update a store.

        Args:
            store_id (int): The id of the store.
            user (User | AnonymousUser | AbstractBaseUser): The user who created the store.
            store_name (str | None): The new name of the store.
            store_type (int | None): The new type of the store.
            store_description (str | None): The new description of the store.

        Returns:
            ShoppingStore: The edited store.

        Raises:
            Store.DoesNotExist: If the store does not exist.
        """

    @abstractmethod
    async def delete_store(
        self,
        store_id: int,
        user: User | AnonymousUser | AbstractBaseUser,
    ) -> None:
        """
        Delete a store.

        Args:
            store_id (int): The id of the store.
            user (User | AnonymousUser | AbstractBaseUser): The user who created the store.

        Raises:
            Store.DoesNotExist: If the store does not exist.
        """

    @abstractmethod
    async def aggregate(
        self,
        user: User | AnonymousUser | AbstractBaseUser | None = None,
    ) -> dict[str, Any]:
        """
        Aggregate stores.

        Args:
            user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.

        Returns:
            dict[str, Any]: The aggregated stores.
        """

    @abstractmethod
    async def does_store_exist(self, store_id: int) -> bool:
        """
        Check if a store exists.

        Args:
            store_id (int): The id of the store.

        Returns:
            bool: True if the store exists, False otherwise.
        """

    @abstractmethod
    async def does_name_exist(self, name: str) -> bool:
        """
        Check if a store name exists.

        Args:
            name (str): The name of the store.

        Returns:
            bool: True if the store name exists, False otherwise.
        """
