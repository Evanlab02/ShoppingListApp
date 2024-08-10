"""Contains the schemas for the stores app."""

import logging

from items.schemas.output import ItemPaginationSchema
from shoppingapp.schemas.shared import BaseContext
from stores.schemas.output import (
    StoreAggregationSchema,
    StorePaginationSchema,
    StoreSchema,
)

log = logging.getLogger(__name__)
log.info("Store context schemas loading...")


class StoreContext(BaseContext):
    """Store context for the store views."""

    store: StoreSchema | None


class StoreDetailContext(StoreContext):
    """Store detail context for detail view."""

    items: ItemPaginationSchema | None


class StoreOverviewContext(BaseContext):
    """Store overview context for the overview views."""

    pagination: StorePaginationSchema
    aggregation: StoreAggregationSchema | None


log.info("Store context schemas loaded.")
