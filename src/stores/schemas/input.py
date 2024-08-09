"""Contains incoming data schemas for the stores app."""

import logging
from datetime import date

from ninja import Schema

log = logging.getLogger(__name__)
log.info("Store input schemas loading...")


class NewStore(Schema):
    """New store schema for incoming data."""

    name: str
    store_type: str | int
    description: str


class StoreDescription(Schema):
    """Store description schema used in the update endpoint."""

    description: str | None = None


class StoreSearch(Schema):
    """Store search schema to filter through stores."""

    ids: list[int] | None = None
    store_types: list[int] | None = None
    created_on: date | None = None
    created_before: date | None = None
    created_after: date | None = None
    updated_on: date | None = None
    updated_before: date | None = None
    updated_after: date | None = None


log.info("Store input schemas loaded.")
