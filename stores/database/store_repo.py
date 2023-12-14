"""Contains store repository functions."""

from asgiref.sync import sync_to_async
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.core.paginator import Paginator

from stores.models import ShoppingStore as Store
from stores.models import ShoppingStorePagination as StorePagination


async def create_store(
    name: str,
    store_type: int,
    description: str,
    user: User | AnonymousUser | AbstractBaseUser,
) -> Store:
    """
    Create a store.

    Args:
        name (str): The name of the store.
        store_type (int): The type of the store.
        description (str): The description of the store.
        username (str): The username of the user creating the store.

    Returns:
        ShoppingStore: The created store.
    """
    store = await Store.objects.acreate(
        name=name,
        store_type=store_type,
        description=description,
        user=user,
    )
    await store.asave()
    return store


@sync_to_async
def _all(page_number: int, stores_per_page: int) -> StorePagination:
    """
    Get all stores.

    Args:
        page_number (int): The page number.

    Returns:
        StorePagination: Stores within a pagination schema.
    """
    stores = Store.objects.all().order_by("-updated_at")
    paginator = Paginator(stores, stores_per_page)
    paginated_page = paginator.get_page(page_number)

    paginated_stores = paginated_page.object_list
    results = [store for store in paginated_stores]
    total = paginator.count
    page = paginated_page.number
    total_pages = paginator.num_pages
    has_previous = paginated_page.has_previous()
    previous_page = paginated_page.previous_page_number() if has_previous else None
    has_next = paginated_page.has_next()
    next_page = paginated_page.next_page_number() if has_next else None

    result = StorePagination(
        stores=results,
        total=total,
        page_number=page,
        total_pages=total_pages,
        has_previous=has_previous,
        previous_page=previous_page,
        has_next=has_next,
        next_page=next_page,
    )

    return result


async def get_stores(
    page_number: int = 1, stores_per_page: int = 10
) -> StorePagination:
    """
    Get all stores.

    Args:
        page (int): The page number.

    Returns:
        list[ShoppingStore]: All stores.
    """
    return await _all(page_number, stores_per_page)
