"""Contains incoming data schemas for the stores app."""

import logging
from datetime import date

from ninja import Schema

log = logging.getLogger(__name__)


class NewStore(Schema):
    """New store schema for incoming data."""

    name: str
    store_type: str | int
    description: str


class StorePatch(Schema):
    """Store patch schema used in the update endpoint."""

    name: str | None = None
    store_type: str | int | None = None
    description: str | None = None


class StoreUpdate(Schema):
    """Store update schema used in the update endpoint."""

    name: str
    store_type: str | int
    description: str


class StoreSearch(Schema):
    """Store search schema to filter through stores."""

    name: str | None = None
    own: bool | None = None
    ids: list[int] | None = None
    store_types: list[int] | None = None
    created_on: date | None = None
    created_before: date | None = None
    created_after: date | None = None
    updated_on: date | None = None
    updated_before: date | None = None
    updated_after: date | None = None
