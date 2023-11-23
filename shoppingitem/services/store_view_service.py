"""Contains the service for the item views."""

from django.core.paginator import Paginator
from django.http import HttpRequest

from ..database import StoreRepository, ItemRepository
from ..models import ShoppingStore

class StoreViewService:
    """The service for the store views."""

    def __init__(self) -> None:
        """Set up the service."""
        self.item_repo = ItemRepository()
        self.store_repo = StoreRepository()

    def _overview_page(self, request: HttpRequest, stores: list[ShoppingStore], is_user_page: bool = False) -> dict:  # type: ignore
        """
        Construct the context for the overview page based on the values passed in.

        Args:
            request(HttpRequest): The request object.
            is_user_page(bool): Whether or not the page is the user page.
            stores(list[ShoppingStore]): The stores to render.

        Returns:
            dict: The context for the overview page.
        """
        total_stores = len(stores)

        page_no = request.GET.get("page", 1)
        paginator = Paginator(stores, 10)
        page = paginator.get_page(page_no)
        stores = page.object_list

        num_pages = paginator.num_pages
        has_next_page = page.has_next()
        has_previous_page = page.has_previous()
        previous_page_no = page.previous_page_number() if has_previous_page else None
        next_page_no = page.next_page_number() if has_next_page else None

        page_title = "Your Stores" if is_user_page else "All Stores"
        table_caption = (
            f"{request.user.username}'s Stores" if is_user_page else "All Stores"
        )
        add_user_col = not is_user_page

        in_store_stores = 0
        online_stores = 0

        if add_user_col:
            in_store_stores = self.store_repo.count_stores_by_type(2)
            online_stores = self.store_repo.count_stores_by_type(1)
            in_store_stores += self.store_repo.count_stores_by_type(3)
            online_stores += self.store_repo.count_stores_by_type(3)
        else:
            user = request.user
            in_store_stores = self.store_repo.count_stores_by_type_for_user(2, user)
            online_stores = self.store_repo.count_stores_by_type_for_user(1, user)
            in_store_stores += self.store_repo.count_stores_by_type_for_user(3, user)
            online_stores += self.store_repo.count_stores_by_type_for_user(3, user)

        return {
            "stores": stores,
            "total": total_stores,
            "page_title": page_title,
            "page_no": page_no,
            "total_pages": num_pages,
            "has_next": has_next_page,
            "has_previous": has_previous_page,
            "previous_page_no": previous_page_no,
            "next_page_no": next_page_no,
            "table_caption": table_caption,
            "add_user_col": add_user_col,
            "in_store_stores": in_store_stores,
            "online_stores": online_stores,
        }
    
    def user_overview_page(self, request: HttpRequest) -> dict:
        """
        Construct the context for the user overview page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the user overview page.
        """
        stores = self.store_repo.get_all_stores_for_user(request.user)
        context = self._overview_page(request, stores, True)
        return context

    def overall_overview_page(self, request: HttpRequest) -> dict:
        """
        Construct the context for the overall overview page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the overall overview page.
        """
        stores = self.store_repo.get_all_stores()
        context = self._overview_page(request, stores)
        return context

    def detail_view(self, request: HttpRequest, store_id: int) -> dict:
        """
        Construct the context for the detail view.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the detail view.
        """
        store = self.store_repo.get_store_by_id(store_id)
        number_of_items = self.item_repo.count_items_from_store(store)
        items = self.item_repo.get_items_from_store(store)

        page_no = request.GET.get("page", 1)
        paginator = Paginator(items, 10)
        page = paginator.get_page(page_no)
        items = page.object_list

        num_pages = paginator.num_pages
        has_next_page = page.has_next()
        has_previous_page = page.has_previous()
        previous_page_no = page.previous_page_number() if has_previous_page else None
        next_page_no = page.next_page_number() if has_next_page else None

        return {
            "store": store,
            "number_of_items": number_of_items,
            "items": items,
            "page_no": page_no,
            "total_pages": num_pages,
            "has_next": has_next_page,
            "has_previous": has_previous_page,
            "previous_page_no": previous_page_no,
            "next_page_no": next_page_no,
        }

    def create_page(self, request: HttpRequest) -> dict:
        """
        Construct the context for the create page.

        Args:
            request(HttpRequest): The request object.

        Returns:
            dict: The context for the create page.
        """
        error = request.GET.get("error")
        return {
            "error": error,
        }

    def create_store(self, request: HttpRequest) -> str:
        """
        Create a store.

        Args:
            request(HttpRequest): The request object.

        Returns:
            str: The url to redirect to.
        """
        user = request.user
        name = request.POST.get("store-input")
        store_type = request.POST.get("store-type-input")
        description = request.POST.get("description-input") or ""

        try:
            store_type = int(store_type)
        except ValueError:
            return "/items/stores/create?error=Store type must be a number."
            
        if store_type not in [1, 2, 3]:
            return "/items/stores/create?error=Invalid store type."
            
        try:
            store = self.store_repo.create_store(name, store_type, description, user)
        except ValueError as error:
            return f"/items/stores/create?error={error}"

        return f"/items/stores/detail/{store.id}"
