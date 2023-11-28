"""Helpers for the shoppinglist app."""

from datetime import datetime

from ..constants import MONTH_MAPPING


def get_months_for_year_until_current_month() -> list[str]:
    """
    Get the months for the current year until the current month.

    Returns:
        list[str]: The months for the current year until the current month.
    """
    current_month = datetime.now().month
    return [MONTH_MAPPING[month] for month in range(1, current_month + 1)]
