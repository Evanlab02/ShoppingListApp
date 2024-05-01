"""Contains shared schemas."""

from django.contrib.auth.models import User
from ninja import ModelSchema, Schema


class UserSchema(ModelSchema):
    """User model schema for outgoing data."""

    class Meta:
        """Meta class for the UserSchema."""

        model = User
        fields = ["username"]


class PaginationSchema(Schema):
    """Pagination schema."""

    total: int = 0
    page_number: int = 1
    total_pages: int = 1
    has_previous: bool = False
    previous_page: int | None = None
    has_next: bool = False
    next_page: int | None = None


class DeleteSchema(Schema):
    """Deletion result schema."""

    message: str
    detail: str


class BaseContext(Schema):
    """Base context schema for views."""

    page_title: str
    is_personal: bool = False
    is_overview: bool = False
    show_advanced_navigation: bool = False
    error: str | None = None
