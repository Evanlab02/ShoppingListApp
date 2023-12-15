"""Contains custom api exceptions for the stores app."""


class InvalidStoreType(Exception):
    """Raised when the store type is invalid."""

    def __init__(self, store_type: str | int) -> None:
        """Initialize the exception."""
        self.store_type = store_type

        if isinstance(store_type, int):
            super().__init__(
                "Internal Conversion Error: Store Type Could Not Be Converted To String."
            )
        else:
            super().__init__(f"Store type '{store_type}' is invalid.")


class StoreAlreadyExists(Exception):
    """Raised when the store name already exists."""

    def __init__(self, store_name: str) -> None:
        """Initialize the exception."""
        self.store_name = store_name
        super().__init__(f"Store '{store_name}' already exists.")
