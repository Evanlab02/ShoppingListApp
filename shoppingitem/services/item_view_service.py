"""Contains the service for the item views."""

from django.core.paginator import Paginator
from django.http import HttpRequest

from ..database import ItemRepository, StoreRepository
from ..helpers.utils import determine_average_price_of_items
from ..models import ShoppingItem


class ItemViewService:
    """The service for the item views."""

    def __init__(self) -> None:
        """Set up the service."""
        self.item_repo = ItemRepository()
        self.store_repo = StoreRepository()

    def _overview_page(
        self,
        request: HttpRequest,
        items: list[ShoppingItem],
        is_user_page: bool = False,
    ) -> dict:  # type: ignore
        """
        Construct the context for the overview page based on the values passed in.

        Args:
            request(HttpRequest): The request object.
            is_user_page(bool): Whether or not the page is the user page.

        Returns:
            dict: The context for the overview page.
        """
        page_title = "Your Shopping Items" if is_user_page else "All Shopping Items"
        table_caption = (
            f"{request.user.username}'s Items" if is_user_page else "All Items"
        )

        total_items = len(items)
        total_price = sum([item.price for item in items])
        average_price = determine_average_price_of_items(total_price, total_items)

        page_no = request.GET.get("page", 1)
        paginator = Paginator(items, 10)
        page = paginator.get_page(page_no)
        items = page.object_list

        has_next_page = page.has_next()
        has_previous_page = page.has_previous()
        previous_page_no = page.previous_page_number() if has_previous_page else None
        next_page_no = page.next_page_number() if has_next_page else None
        num_pages = paginator.num_pages

        add_user_col = not is_user_page

        return {
            "items": items,
            "total": total_items,
            "total_price": total_price,
            "average_price": average_price,
            "page_title": page_title,
            "page_no": page_no,
            "total_pages": num_pages,
            "has_next": has_next_page,
            "has_previous": has_previous_page,
            "previous_page_no": previous_page_no,
            "next_page_no": next_page_no,
            "table_caption": table_caption,
            "add_user_col": add_user_col,
        }

    def overall_overview_page(self, request: HttpRequest) -> dict:  # type: ignore
        """
        Construct the context for the overall overview page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the overall overview page.
        """
        items = self.item_repo.get_all_items()
        context = self._overview_page(request, items, False)
        return context

    def user_overview_page(self, request: HttpRequest) -> dict:  # type: ignore
        """
        Construct the context for the user overview page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the user overview page.
        """
        items = self.item_repo.get_all_items_for_user(request.user)
        context = self._overview_page(request, items, True)
        return context

    def detail_page(self, item_id: int) -> dict:  # type: ignore
        """
        Construct the context for the detail page.

        Args:
            item_id(int): The id of the item to get the detail page for.

        Returns:
            dict: The context for the detail page.
        """
        item = self.item_repo.get_item_by_id(item_id)
        number_of_lists = self.item_repo.get_number_of_lists_linked_to_item(item)

        return {
            "item": item,
            "number_of_lists": number_of_lists,
        }

    def create_page(self, request: HttpRequest) -> dict:  # type: ignore
        """
        Construct the context for the create page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the create page.
        """
        error = request.GET.get("error")
        stores = self.store_repo.get_all_stores()
        return {
            "stores": stores,
            "error": error,
        }

    def create_item(self, request: HttpRequest) -> str:
        """
        Attempt to create a item and return the redirect url.

        Args:
            request(HttpRequest): The request object.

        Returns:
            str: The redirect url.
        """
        name = request.POST.get("item-input")
        store_name = request.POST.get("store-input")
        price = request.POST.get("price-input")

        if not name or not store_name or not price:
            return "/items/create?error=Please fill in all fields."

        store = self.store_repo.get_store_by_name(store_name)
        clone_exists = self.item_repo.does_item_exist(name, store)

        if clone_exists:
            return "/items/create?error=Item already exists."
        elif not price.isnumeric():
            return "/items/create?error=Price must be a number."
        elif float(price) <= 0:
            return "/items/create?error=Price cannot be negative and must be greater than 0."

        item = self.item_repo.create_item(name, store, float(price), request.user)
        return f"/items/detail/{item.id}"
