"""Contains the dashboard router."""

from django.http import HttpRequest
from ninja import Router

from authentication.auth.api_key import ApiKey
from authentication.auth.session_auth import SessionAuth
from dashboard.schemas.output import (
    DashboardHistory,
    DashboardOverview,
    DashboardRecentItems,
)
from dashboard.schemas.sub_output import BarChartDataset

session_dashboard_router = Router(tags=["Session Dashboard"], auth=SessionAuth(csrf=True))
token_dashboard_router = Router(tags=["Token Dashboard"], auth=ApiKey())


async def _dashboard_overview() -> DashboardOverview:
    """Get the dashboard overview."""
    return DashboardOverview(
        total=0,
        total_price=0,
        budget_remaining=0,
        average_item_price=0,
    )


async def _dashboard_recent_items() -> DashboardRecentItems:
    """Get the dashboard recent items."""
    return DashboardRecentItems(items=[])


async def _dashboard_history() -> DashboardHistory:
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


@session_dashboard_router.get("/overview")
async def session_dashboard_overview(request: HttpRequest) -> DashboardOverview:
    """Get the dashboard overview."""
    return await _dashboard_overview()


@session_dashboard_router.get("/recent/items")
async def session_dashboard_recent_items(request: HttpRequest) -> DashboardRecentItems:
    """Get the dashboard recent items."""
    return await _dashboard_recent_items()


@session_dashboard_router.get("/history")
async def session_dashboard_history(request: HttpRequest) -> DashboardHistory:
    """Get the dashboard history."""
    return await _dashboard_history()


@token_dashboard_router.get("/overview")
async def token_dashboard_overview(request: HttpRequest) -> DashboardOverview:
    """Get the dashboard overview."""
    return await _dashboard_overview()


@token_dashboard_router.get("/recent/items")
async def token_dashboard_recent_items(request: HttpRequest) -> DashboardRecentItems:
    """Get the dashboard recent items."""
    return await _dashboard_recent_items()


@token_dashboard_router.get("/history")
async def token_dashboard_history(request: HttpRequest) -> DashboardHistory:
    """Get the dashboard history."""
    return await _dashboard_history()
