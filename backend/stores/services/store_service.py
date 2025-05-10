"""Contains the store service."""

from typing import Any, Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.constants import STORE_TYPE_MAPPING
from stores.database.store_repo import StoreRepo
from stores.errors.exceptions import (
    InvalidStoreType,
    StoreAlreadyExists,
    StoreDoesNotExist,
)
from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore
from stores.schemas.output import StorePaginationSchema
from stores.services.interfaces.i_store_service import IStoreService


class StoreService(IStoreService):
    """Store service."""

    def __init__(self) -> None:
        """Initialize the store service."""
        self.repo = StoreRepo()
        super().__init__()

    def __get_store_type_value(self, store_type_label: str) -> int:
        """
        Get the store type value.

        Args:
            store_type_label (str): The store type label.

        Returns:
            int: The store type value.

        Raises:
            InvalidStoreType: If the store type is invalid.
        """
        for key, value in STORE_TYPE_MAPPING.items():
            if value == store_type_label:
                return key

        self.log.warning("Failed store type conversion to value.")
        raise InvalidStoreType(store_type_label)

    def __get_store_type(self, store_type: int | str) -> int:
        """
        Get the store type.

        Args:
            store_type (int | str): The store type.

        Returns:
            int: The store type value.

        Raises:
            InvalidStoreType: If the store type is invalid.
        """
        if isinstance(store_type, str):
            return self.__get_store_type_value(store_type)

        if store_type in STORE_TYPE_MAPPING.keys():
            return store_type

        self.log.warning("Failed store type conversion to value.")
        raise InvalidStoreType(store_type)

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
        name = new_store.name
        store_type = new_store.store_type
        description = new_store.description

        store_type_value = self.__get_store_type(store_type)

        if await self.repo.does_name_exist(name):
            self.log.warning("Store with this name already exists...")
            raise StoreAlreadyExists(name)

        return await self.repo.create_store(
            name=name,
            store_type=store_type_value,
            description=description,
            user=user,
        )

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
        return await self.repo.get_stores(
            page_number,
            limit,
            user,
            sort,
            sort_dir,
        )

    async def get_store(self, store_id: int) -> Store:
        """
        Get the store details.

        Args:
            store_id (int): The id of the store.

        Returns:
            Store: The store.

        Raises:
            StoreDoesNotExist: If the store does not exist.
        """
        try:
            return await self.repo.get_store(store_id)
        except Store.DoesNotExist:
            self.log.warning(f"Store with id {store_id} does not exist.")
            raise StoreDoesNotExist(store_id)
