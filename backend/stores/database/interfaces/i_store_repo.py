"""Contains interfaces for the store repositories."""

import logging
from abc import ABC, abstractmethod


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
