"""Contains the schemas for the stores app."""

from ninja import Schema

from stores.schemas.output import StorePaginationSchema, StoreSchema


class BaseContext(Schema):
    """Base context schema for views."""

    page_title: str
    is_personal: bool = False
    is_overview: bool = False
    show_advanced_navigation: bool = False
    error: str | None = None


class StoreDetailContext(BaseContext):
    """Store detail context for detail view."""

    store: StoreSchema


class StorePaginationContext(BaseContext):
    """Store pagination context for the overview views."""

    pagination: StorePaginationSchema
