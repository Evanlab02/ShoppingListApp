"""Contains the budget repository."""

from datetime import datetime

from django.contrib.auth.models import User

from ..helpers import get_months_for_year_until_current_month
from ..models import ShoppingBudget
from .list_repo import ShoppingListRepository


class BudgetRepository:
    """The budget repository."""

    def __init__(self) -> None:
        """Initialize the budget repository."""
        self.list_repo = ShoppingListRepository()

    def get_total_budget_of_shopping_list(self, list_id: int) -> float:
        """
        Return the total budget of a shopping list.

        Args:
            list_id (int): The shopping list ID.

        Returns:
            float: The total budget of a shopping list.
        """
        budget = ShoppingBudget.objects.get(shopping_list=list_id)
        budget_amount = float(0)

        if budget is not None:
            budget_amount = float(budget.amount)

        return budget_amount

    def get_budget_remaining_of_shopping_list(self, list_id: int) -> float:
        """
        Return the budget remaining of a shopping list.

        Args:
            list_id (int): The shopping list ID.

        Returns:
            float: The budget remaining of a shopping list.
        """
        total_budget = self.get_total_budget_of_shopping_list(list_id)
        total_price = self.list_repo.get_total_price_of_items_on_shopping_list(list_id)

        budget_remaining = float(0)

        if total_budget > 0:
            budget_remaining = total_budget - total_price

        if budget_remaining < 0:
            budget_remaining = float(0)

        return budget_remaining

    def get_budgets_for_many_shopping_lists(
        self, list_ids: list[int]
    ) -> list[ShoppingBudget]:
        """
        Get the budgets for many shopping lists.

        Args:
            list_ids (list[int]): The shopping list IDs.

        Returns:
            list[ShoppingBudget]: The budgets for many shopping lists.
        """
        budgets = ShoppingBudget.objects.filter(shopping_list__in=list_ids)
        list_of_budgets = [budget for budget in budgets]
        return list_of_budgets

    def get_price_history_current_year_for_user(
        self, user: User
    ) -> dict[str, list[str] | list[float] | list[int]]:
        """
        Get the price history for the current year for a user.

        Args:
            user (User): The user.

        Returns:
            dict[str, list]: The price history for the current year for a user.
        """
        current_year = datetime.now().year
        current_year_months = get_months_for_year_until_current_month()

        list_data = [float(0) for _ in current_year_months]
        budget_data = [float(0) for _ in current_year_months]

        shopping_lists = self.list_repo.get_lists_created_in_year_for_user(
            user=user, year=current_year
        )

        list_ids = [shopping_list.id for shopping_list in shopping_lists]

        for shopping_list in shopping_lists:
            end_date = shopping_list.end_date
            month = end_date.month

            total_price = self.list_repo.get_total_price_of_items_on_shopping_list(
                shopping_list.id
            )
            list_data[month - 1] += total_price

        budgets = self.get_budgets_for_many_shopping_lists(list_ids)

        for shopping_budget in budgets:
            end_date = shopping_budget.shopping_list.end_date
            month = end_date.month
            budget_data[month - 1] += float(shopping_budget.amount)

        return {
            "months": current_year_months,
            "list_data": list_data,
            "budget_data": budget_data,
        }
