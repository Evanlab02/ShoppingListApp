"""Contains interfaces for the store services."""

import logging
from abc import ABC, abstractmethod

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User

from stores.models import ShoppingStore as Store
from stores.schemas.input import NewStore


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
