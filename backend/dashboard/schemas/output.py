"""Contains the outgoing schemas from the dashboard app."""

import logging

from ninja import Schema

from dashboard.schemas.sub_output import BarChartDataset
from items.schemas.output import ItemSchema

log = logging.getLogger(__name__)
log.info("Loading dashboard output schemas...")


class DashboardOverview(Schema):
    """Dashboard overview schema."""

    total: int | None
    total_price: float | None
    budget_remaining: float | None
    average_item_price: float | None


class DashboardRecentItems(Schema):
    """Dashboard recent items schema."""

    items: list[ItemSchema]


class DashboardHistory(Schema):
    """Dashboard history schema."""

    labels: list[str]
    data: list[BarChartDataset]


log.info("Loaded dashboard output schemas.")
