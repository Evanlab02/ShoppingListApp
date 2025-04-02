"""Contains interfaces for the store repositories."""

import logging
from abc import ABC, abstractmethod

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore as Store


class IStoreRepo(ABC):
    """Interface for the store repository."""

    def __init__(self) -> None:
        """Initialize the store repository."""
        self.log = logging.getLogger(__name__)
        super().__init__()

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
