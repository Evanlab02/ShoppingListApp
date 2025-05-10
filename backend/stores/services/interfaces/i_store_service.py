"""Contains interfaces for the store services."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore, StoreSearch
from stores.schemas.output import StorePaginationSchema


class IStoreService(ABC):
    """Interface for the store services."""

    def __init__(self) -> None:
        """Initialize the store service."""
        self.log = logging.getLogger(__name__)

    @abstractmethod
    async def create(
        self,
        new_store: NewStore,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> Store:
        """
        Create a new store.

        Args:
            new_store (NewStore): The new store data.

        Returns:
            Store: The created store.

        Raises:
            InvalidStoreType: If the store type is invalid.
            StoreAlreadyExists: If the store already exists.
        """

    @abstractmethod
    async def get_stores(
        self,
        limit: int = 10,
        page_number: int = 1,
        user: Any | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Get the stores.

        Args:
            limit (int): The limit of stores per page, defaults 10.
            page_number (int): The page number, defaults to 1.
            user (User): User who created the stores.
            sort (str | None): The field to sort by.
            sort_dir (str | None): The direction to sort in.

        Returns:
            StorePaginationSchema: The stores in a paginated format.
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
            page_number (int): The page number, defaults to 1.
            stores_per_page (int): The number of stores per page, defaults to 10.
            name (str | None): The name of the store.
            user (User | None): The user who created the stores.

        Returns:
            StorePaginationSchema: The stores in a paginated format.
        """

    @abstractmethod
    async def get_store(self, store_id: int) -> Store:
        """
        Get the store detail.

        Args:
            store_id (int): The id of the store.

        Returns:
            Store: The store.

        Raises:
            StoreDoesNotExist: If the store does not exist.
        """
