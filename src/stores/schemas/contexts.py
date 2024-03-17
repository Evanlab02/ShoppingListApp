"""Contains the schemas for the stores app."""

from shoppingapp.schemas.shared import BaseContext
from stores.schemas.output import (
    StoreAggregationSchema,
    StorePaginationSchema,
    StoreSchema,
)


class StoreDetailContext(BaseContext):
    """Store detail context for detail view."""

    store: StoreSchema


class StoreOverviewContext(BaseContext):
    """Store overview context for the overview views."""

    pagination: StorePaginationSchema
    aggregation: StoreAggregationSchema | None
