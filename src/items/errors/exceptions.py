"""Contains exceptions for the items app."""


class ItemAlreadyExists(Exception):
    """Raised when the item already exists."""

    def __init__(self, item_name: str, store_name: str) -> None:
        """Initialize the exception."""
        self.item_name = item_name
        self.store_name = store_name
        super().__init__(f"Item ('{item_name}') already exists @ '{store_name}'.")


class ItemDoesNotExist(Exception):
    """Raised when the item does not exist."""

    def __init__(self, item_id: int) -> None:
        """Initialize the exception."""
        self.item_id = item_id
        super().__init__(f"Item with id '{item_id}' does not exist.")
