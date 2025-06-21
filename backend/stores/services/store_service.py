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
from stores.schemas.input import NewStore, StoreSearch
from stores.schemas.output import StoreAggregationSchema, StorePaginationSchema
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
        return await self.repo.search_stores(
            page_number=page_number,
            stores_per_page=stores_per_page,
            name=name,
            user=user,
            search=search,
            sort=sort,
            sort_dir=sort_dir,
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

    async def update(
        self,
        store_id: int,
        user: User | AnonymousUser | AbstractBaseUser,
        store_name: str | None = None,
        store_type: int | str | None = None,
        store_description: str | None = None,
    ) -> Store:
        """
        Update a store.

        Args:
            store_id (int): The id of the store.
            user (User | AbstractBaseUser | AnonymousUser): The user who is updating the store.
            store_name (str | None): The new store name.
            store_type (int | str | None): The new store type.
            store_description (str | None): The new store description.

        Returns:
            Store: The updated store.

        Raises:
            StoreDoesNotExist: If the store does not exist.
            StoreAlreadyExists: If a store with the new name already exists.
        """
        try:
            store = await self.repo.get_store(store_id=store_id)

            name = store.name
            updating_name = False

            if store_name and store_name != name:
                updating_name = True
                name = store_name

            if updating_name and await self.repo.does_name_exist(name):
                self.log.warning("Store with this name already exists...")
                raise StoreAlreadyExists(name)

            if store_type:
                store_type = self.__get_store_type(store_type)
            else:
                store_type = store.store_type

            return await self.repo.update_store(
                store_id=store_id,
                user=user,
                store_name=name,
                store_type=store_type,
                store_description=store_description,
            )
        except Store.DoesNotExist:
            self.log.warning(f"Store with id {store_id} does not exist.")
            raise StoreDoesNotExist(store_id)

    async def delete(self, store_id: int, user: User | AnonymousUser | AbstractBaseUser) -> None:
        """
        Delete a store.

        Args:
            store_id (int): The id of the store you wish to delete.
            user (User): The user that owns this store,
            to prevent users deleting other users stores.

        Returns:
            None

        Raises:
            StoreDoesNotExist: If the store does not exist.
        """
        try:
            await self.repo.delete_store(store_id, user)
        except Store.DoesNotExist:
            self.log.warning(f"Store with id {store_id} does not exist.")
            raise StoreDoesNotExist(store_id)

    async def aggregate(
        self,
        user: User | AnonymousUser | AbstractBaseUser | None = None,
        name: str | None = None,
        search: StoreSearch | None = None,
    ) -> StoreAggregationSchema:
        """
        Aggregate the stores.

        Args:
            user (User | AnonymousUser | AbstractBaseUser | None): The user who created the stores.

        Returns:
            dict[str, Any]: The aggregated stores.
        """
        aggregation = await self.repo.aggregate(user=user, name=name, search=search)
        aggregation["combined_online_stores"] = (
            aggregation["online_stores"] + aggregation["combined_stores"]
        )
        aggregation["combined_in_store_stores"] = (
            aggregation["in_store_stores"] + aggregation["combined_stores"]
        )
        return StoreAggregationSchema(**aggregation)
