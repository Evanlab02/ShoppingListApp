"""Contains incoming data schemas for the stores app."""

from ninja import Schema


class NewStore(Schema):
    """New store schema for incoming data."""

    name: str
    store_type: str
    description: str
