"""Contains the models for the stores app."""

from django.contrib.auth.models import User
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    Model,
    TextField,
)

from stores.constants import STORE_TYPE_CHOICES


class ShoppingStore(Model):
    """Model for a shopping store."""

    name = CharField(max_length=100, unique=True)
    store_type = IntegerField(choices=STORE_TYPE_CHOICES)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    user = ForeignKey(User, on_delete=CASCADE)

    def __str__(self) -> str:
        """Return a string representation of the shopping store."""
        return f"{self.name}"


class ShoppingStorePagination:
    """Pagination Class for ShoppingStore."""

    stores: list[ShoppingStore]
    total: int
    page_number: int
    total_pages: int
    has_previous: bool
    previous_page: int | None
    has_next: bool
    next_page: int | None

    def __init__(
        self,
        stores: list[ShoppingStore],
        total: int,
        page_number: int,
        total_pages: int,
        has_previous: bool,
        previous_page: int | None,
        has_next: bool,
        next_page: int | None,
    ) -> None:
        """Initialize the class."""
        self.stores = stores
        self.total = total
        self.page_number = page_number
        self.total_pages = total_pages
        self.has_previous = has_previous
        self.previous_page = previous_page
        self.has_next = has_next
        self.next_page = next_page
