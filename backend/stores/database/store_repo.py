"""Contains the store repository."""

from math import ceil
from typing import Literal

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import QuerySet

from stores.database.interfaces.i_store_repo import IStoreRepo
from stores.models import ShoppingStore as Store
from stores.schemas.input import StoreSearch
from stores.schemas.output import StorePaginationSchema, StoreSchema


class StoreRepo(IStoreRepo):
    """Store repository."""

    def __init__(self) -> None:
        """Initialize the store repository."""
        super().__init__()

    async def create_store(
        self,
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
            user (User | AnonymousUser | AbstractBaseUser): The user who created the store.

        Returns:
            ShoppingStore: The created store.
        """
        return await Store.objects.acreate(
            name=name,
            store_type=store_type,
            description=description,
            user=user,  # type: ignore
        )

    def __search(
        self,
        search: StoreSearch,
        queryset: QuerySet[Store],
    ) -> QuerySet[Store]:
        """
        Search for stores.

        Args:
            search (StoreSearch | None): The search object containing the search parameters.
            queryset (QuerySet[Store] | None): The queryset to search from.

        Returns:
            QuerySet[Store]: The filtered stores.
        """
        if search.ids:
            queryset = queryset.filter(id__in=search.ids)
        if search.store_types:
            queryset = queryset.filter(store_type__in=search.store_types)
        if search.created_on:
            queryset = queryset.filter(created_at__date=search.created_on)
        if search.created_before:
            queryset = queryset.filter(created_at__date__lte=search.created_before)
        if search.created_after:
            queryset = queryset.filter(created_at__date__gte=search.created_after)
        if search.updated_on:
            queryset = queryset.filter(updated_at__date=search.updated_on)
        if search.updated_before:
            queryset = queryset.filter(updated_at__date__lte=search.updated_before)
        if search.updated_after:
            queryset = queryset.filter(updated_at__date__gte=search.updated_after)

        return queryset

    def __filter(
        self,
        name: str | None = None,
        user: User | None = None,
        search: StoreSearch | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> QuerySet[Store]:
        """
        Filter stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            name (str | None): The name of the store.
            search (StoreSearch | None): The search object containing the search parameters.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            QuerySet[Store]: The filtered stores.
        """
        stores = Store.objects.select_related("user").all()

        if name:
            stores = stores.filter(name__icontains=name)
        if user:
            stores = stores.filter(user=user)
        if search:
            stores = self.__search(search=search, queryset=stores)

        sort_field = sort or "updated_at"
        prefix = "" if sort_dir == "asc" else "-"
        stores = stores.order_by(f"{prefix}{sort_field}")

        return stores

    async def __paginate(
        self,
        page_number: int = 1,
        stores_per_page: int = 10,
        name: str | None = None,
        user: User | None = None,
        search: StoreSearch | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Paginate stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            name (str | None): The name of the store.
            search (StoreSearch | None): The search object containing the search parameters.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            StorePaginationSchema: The paginated stores.
        """
        stores = self.__filter(name=name, user=user, search=search, sort=sort, sort_dir=sort_dir)

        total = await stores.acount()
        total_pages = ceil(total / stores_per_page)

        start = (page_number - 1) * stores_per_page
        end = start + stores_per_page

        if start > total:
            page_number = total_pages
            start = (page_number - 1) * stores_per_page
            end = start + stores_per_page

        paginated_stores = stores[start:end]
        results = [StoreSchema.from_orm(store) async for store in paginated_stores]

        has_previous = page_number > 1
        previous_page = page_number - 1 if page_number > 1 else None
        has_next = end < total
        next_page = page_number + 1 if end < total else None

        return StorePaginationSchema(
            stores=results,
            total=total,
            page_number=page_number,
            total_pages=total_pages,
            has_previous=has_previous,
            previous_page=previous_page,
            has_next=has_next,
            next_page=next_page,
        )

    async def get_stores(
        self,
        page_number: int = 1,
        stores_per_page: int = 10,
        user: User | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Get all stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            user (User | AnonymousUser | AbstractBaseUser | None): The user who created the store.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            StorePaginationSchema: The paginated stores.
        """
        return await self.__paginate(
            page_number=page_number,
            stores_per_page=stores_per_page,
            user=user,
            sort=sort,
            sort_dir=sort_dir,
        )

    async def search_stores(
        self,
        page_number: int = 1,
        stores_per_page: int = 10,
        name: str | None = None,
        user: User | None = None,
        search: StoreSearch | None = None,
        sort: Literal["name", "created_on", "updated_on"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> StorePaginationSchema:
        """
        Search for stores.

        Args:
            page_number (int): The page number.
            stores_per_page (int): The number of stores per page.
            name (str | None): The name of the store.
            user (User | None): The user who created the store.
            search (StoreSearch | None): The search object containing the search parameters.
            sort (Literal["name", "created_on", "updated_on"] | None): The sort order.
            sort_dir (Literal["asc", "desc"] | None): The sort direction.

        Returns:
            StorePaginationSchema: The paginated stores.
        """
        return await self.__paginate(
            page_number=page_number,
            stores_per_page=stores_per_page,
            name=name,
            user=user,
            search=search,
            sort=sort,
            sort_dir=sort_dir,
        )

    async def does_store_exist(self, store_id: int) -> bool:
        """
        Check if a store exists.

        Args:
            store_id (int): The id of the store.

        Returns:
            bool: True if the store exists, False otherwise.
        """
        return await Store.objects.filter(id=store_id).aexists()
