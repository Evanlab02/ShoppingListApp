"""Contains interfaces for the store services."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore
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
