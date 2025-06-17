"""Contains contexts for the rendering in the items app."""

import logging

from items.schemas.output import ItemAggregationSchema, ItemPaginationSchema, ItemSchema
from shoppingapp.schemas.shared import BaseContext

log = logging.getLogger(__name__)


class ItemOverviewContext(BaseContext):
    """Item overview context."""

    pagination: ItemPaginationSchema
    aggregation: ItemAggregationSchema


class ItemDetailContext(BaseContext):
    """Item detail context."""

    item: ItemSchema
