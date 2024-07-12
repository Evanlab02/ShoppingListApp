"""Bar chart dataset schema."""

from ninja import Schema


class BarChartDataset(Schema):
    """Bar chart dataset schema."""

    label: str
    data: list[int]
