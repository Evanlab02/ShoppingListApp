"""Contains the store repository for the shoppingitem app."""

from django.contrib.auth.models import User

from ..models import ShoppingStore


class StoreRepository:
    """
    The store repository class.

    Methods:
        count_stores_by_type(store_type: int) -> int
        count_stores_by_type_for_user(store_type: int, user: User) -> int
        create_store(name: str, store_type: int, description: str, user: User) -> ShoppingStore
        does_store_exist(name: str) -> bool
        edit_store(store_id: int, name: str, store_type: int, description: str) -> ShoppingStore
        get_all_stores() -> list[ShoppingStore]
        get_all_stores_for_user(user: User) -> list[ShoppingStore]
        get_store_by_id(store_id: int) -> ShoppingStore
        get_store_by_name(name: str) -> ShoppingStore
    """

    def _validate_name(self, name: str) -> None:
        """
        Validate a store name.

        Args:
            name (str): The name of the store to validate.

        Raises:
            ValueError: If the name is empty or already exists.
        """
        if name == "":
            raise ValueError("Store name cannot be empty.")
        elif self.does_store_exist(name):
            raise ValueError(f"Store with name '{name}' already exists.")

    def _validate_store_type(self, store_type: int) -> None:
        """
        Validate a store type.

        Args:
            store_type (int): The type of store to validate.

        Raises:
            TypeError: If the store type is not an integer.
            ValueError: If the store type is invalid.
        """
        if not isinstance(store_type, int):
            raise TypeError("Store type should be an integer.")
        elif store_type not in [1, 2, 3]:
            raise ValueError(f"Store type '{store_type}' is invalid.")

    def count_stores_by_type(self, store_type: int) -> int:
        """
        Count the number of stores by type.

        Args:
            store_type (int): The type of store to count.

        Returns:
            int: The number of stores by type.
        """
        return ShoppingStore.objects.filter(store_type=store_type).count()

    def count_stores_by_type_for_user(self, store_type: int, user: User) -> int:
        """
        Count the number of stores by type for a user.

        Args:
            store_type (int): The type of store to count.
            user (User): The user to count the stores for.

        Returns:
            int: The number of stores by type for a user.
        """
        return ShoppingStore.objects.filter(store_type=store_type, user=user).count()

    def create_store(
        self, name: str, store_type: int, description: str, user: User
    ) -> ShoppingStore:
        """
        Create a store.

        Args:
            name (str): The name of the store to create.
            store_type (int): The type of store to create.
            description (str): The description of the store to create.
            user (User): The user to create the store for.

        Returns:
            ShoppingStore: The created store.

        Raises:
            RepositoryError: If the name or store type is invalid.
        """
        self._validate_name(name)
        self._validate_store_type(store_type)

        store = ShoppingStore(
            name=name, store_type=store_type, description=description, user=user
        )
        store.save()
        return store

    def does_store_exist(self, name: str) -> bool:
        """
        Check if a store exists.

        Args:
            name (str): The name of the store to check.

        Returns:
            bool: True if the store exists, False otherwise.
        """
        return ShoppingStore.objects.filter(name=name).exists()

    def edit_store(
        self, store_id: int, name: str, store_type: int, description: str
    ) -> ShoppingStore:
        """
        Edit a store.

        Args:
            store_id (int): The id of the store to edit.
            name (str): The name of the store to edit.
            store_type (int): The type of store to edit.
            description (str): The description of the store to edit.

        Returns:
            ShoppingStore: The edited store.
        """
        self._validate_name(name)
        self._validate_store_type(store_type)

        store = self.get_store_by_id(store_id)
        store.name = name
        store.store_type = store_type
        store.description = description
        store.save()
        return store

    def get_all_stores(self) -> list[ShoppingStore]:
        """
        Get all stores.

        Returns:
            list[ShoppingStore]: All stores.
        """
        stores = ShoppingStore.objects.all().order_by("-updated_at")
        list_of_stores = [store for store in stores]
        return list_of_stores

    def get_all_stores_for_user(self, user: User) -> list[ShoppingStore]:
        """
        Get all stores for a user.

        Args:
            user (User): The user to get the stores for.

        Returns:
            list[ShoppingStore]: The stores for the user.
        """
        stores = ShoppingStore.objects.filter(user=user).order_by("-updated_at")
        list_of_stores = [store for store in stores]
        return list_of_stores

    def get_store_by_id(self, store_id: int) -> ShoppingStore:
        """
        Get a store by id.

        Args:
            store_id (int): The id of the store to get.

        Returns:
            ShoppingStore: The store with the id.
        """
        return ShoppingStore.objects.get(id=store_id)

    def get_store_by_name(self, name: str) -> ShoppingStore:
        """
        Get a store by name.

        Args:
            name (str): The name of the store to get.

        Returns:
            ShoppingStore: The store with the name.
        """
        return ShoppingStore.objects.get(name=name)
