"""Contains the store repository."""

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.database.interfaces.i_store_repo import IStoreRepo
from stores.models import ShoppingStore as Store


class StoreRepo(IStoreRepo):
    """Store repository."""

    def __init__(self) -> None:
        """Initialize the store repository."""
        super().__init__()

    async def does_store_exist(self, store_id: int) -> bool:
        """
        Check if a store exists.

        Args:
            store_id (int): The id of the store.

        Returns:
            bool: True if the store exists, False otherwise.
        """
        return await Store.objects.filter(id=store_id).aexists()

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
        return await Store.objects.acreate(
            name=name,
            store_type=store_type,
            description=description,
            user=user,  # type: ignore
        )
