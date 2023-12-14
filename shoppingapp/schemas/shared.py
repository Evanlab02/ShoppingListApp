"""Contains shared schemas."""

from ninja import Schema


class PaginationSchema(Schema):
    """Pagination schema."""

    total: int
    page: int
    total_pages: int
    has_previous: bool
    previous_page: int | None
    has_next: bool
    next_page: int | None
