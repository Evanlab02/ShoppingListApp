"""Bar chart dataset schema."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)


class BarChartDataset(Schema):
    """Bar chart dataset schema."""

    label: str
    data: list[int]
