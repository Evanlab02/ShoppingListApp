"""Contains the dashboard router."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.session_auth import SessionAuth
from dashboard.schemas.output import (
    DashboardHistory,
    DashboardOverview,
    DashboardRecentItems,
)
from dashboard.schemas.sub_output import BarChartDataset

dashboard_router = Router(tags=["Dashboard"], auth=SessionAuth())


@dashboard_router.get("/overview")
async def dashboard_overview(request: HttpRequest) -> DashboardOverview:
    """Get the dashboard overview."""
    return DashboardOverview(
        total=0,
        total_price=0,
        budget_remaining=0,
        average_item_price=0,
    )


@dashboard_router.get("/recent/items")
async def dashboard_recent_items(request: HttpRequest) -> DashboardRecentItems:
    """Get the dashboard recent items."""
    return DashboardRecentItems(items=[])


@dashboard_router.get("/history")
async def dashboard_history(request: HttpRequest) -> DashboardHistory:
    """Get the dashboard history."""
    DATA_SET_PRICE = BarChartDataset(
        label="Price",
        data=[65, 59, 80, 81, 56, 55],
    )

    DATA_SET_BUDGET = BarChartDataset(
        label="Budget",
        data=[28, 48, 40, 19, 86, 27],
    )

    return DashboardHistory(
        labels=[
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
        ],
        data=[DATA_SET_PRICE, DATA_SET_BUDGET],
    )
