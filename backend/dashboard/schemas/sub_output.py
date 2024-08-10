"""Bar chart dataset schema."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)
log.info("Loading dashboard sub output schemas...")


class BarChartDataset(Schema):
    """Bar chart dataset schema."""

    label: str
    data: list[int]


log.info("Loaded dashboard sub output schemas.")
