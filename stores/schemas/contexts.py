"""Contains the schemas for the stores app."""

from ninja import Schema


class BaseContext(Schema):
    """Base context schema for incoming data."""

    page_title: str
    is_personal: bool = False
    show_advanced_navigation: bool = False
    error: str | None = None
