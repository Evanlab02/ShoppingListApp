"""Contains all the shopping list app's routes for dashboard pages."""

from django.http import HttpRequest
from ninja import Router

from authenticationapp.auth import ApiKey
from shoppingitem.database import ItemRepository

from ..database import BudgetRepository, ShoppingListRepository
from ..schemas.output import (
    DashboardCurrentSchema,
    DashboardHistorySchema,
    DashboardRecentSchema,
)

dashboard_router = Router(tags=["Dashboard Routes"], auth=ApiKey())

ITEM_REPO = ItemRepository()
LIST_REPOSITORY = ShoppingListRepository()
BUDGET_REPOSITORY = BudgetRepository()


@dashboard_router.get("current", response={200: DashboardCurrentSchema})
def get_current_shopping_list_dashboard_data(
    request: HttpRequest,
) -> DashboardCurrentSchema:
    """
    Return the current shopping list dashboard data.

    Args:
        request (HttpRequest): The request object.

    Returns:
        DashboardCurrentSchema: The current shopping list dashboard data.
    """
    user = request.user
    shopping_list = LIST_REPOSITORY.get_current(user)  # type: ignore

    if shopping_list is None:
        return DashboardCurrentSchema()

    total = LIST_REPOSITORY.get_number_of_items_on_shopping_list(shopping_list.id)
    price = LIST_REPOSITORY.get_total_price_of_items_on_shopping_list(shopping_list.id)
    average_price = LIST_REPOSITORY.get_average_price_of_items_on_shopping_list(
        shopping_list.id
    )
    budget_remaining = BUDGET_REPOSITORY.get_budget_remaining_of_shopping_list(
        shopping_list.id
    )

    return DashboardCurrentSchema(
        total=total,
        total_price=price,
        budget_remaining=budget_remaining,
        average_item_price=average_price,
    )


@dashboard_router.get("recent", response={200: DashboardRecentSchema})
def get_recent_5_items(request: HttpRequest) -> DashboardRecentSchema:
    """
    Return the 5 most recent shopping items.

    Args:
        request (HttpRequest): The request object.

    Returns:
        DashboardRecentSchema: The 5 most recent shopping items.
    """
    recent_items = ITEM_REPO.get_recent_items()
    return DashboardRecentSchema(recent_items=recent_items)


@dashboard_router.get("history", response={200: DashboardHistorySchema})
def get_shopping_list_history(request: HttpRequest) -> DashboardHistorySchema:
    """
    Return the shopping list history.

    Args:
        request (HttpRequest): The request object.

    Returns:
        DashboardHistorySchema: The shopping list history.
    """
    user = request.user

    history = BUDGET_REPOSITORY.get_price_history_current_year_for_user(user=user)  # type: ignore

    return DashboardHistorySchema(
        labels=history.get("months", []),
        datasets=[
            {"label": "Price", "data": history.get("list_data", [])},
            {"label": "Budget", "data": history.get("budget_data", [])},
        ],
    )
