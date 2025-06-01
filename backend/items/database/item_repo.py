"""Contains item repository functions."""

from math import ceil
from typing import Any, Literal, no_type_check

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser, User
from django.db.models import Avg, Count, Max, Min, QuerySet, Sum

from items.database.interfaces.i_item_repo import IItemRepo
from items.models import ShoppingItem as Item
from items.schemas.input import ItemSearchSchema
from items.schemas.output import ItemPaginationSchema, ItemSchema


class ItemRepo(IItemRepo):
    """Item repository."""

    def __init__(self) -> None:
        """Initialize the item repository."""
        super().__init__()

    def __search(self, items: QuerySet[Item], search: ItemSearchSchema) -> QuerySet[Item]:
        """
        Search items using the search schema object.

        Args:
            items (QuerySet[Item]): The query set to search upon.
            search (ItemSearchSchema): The search object to use.

        Returns:
            items (QuerySet[Item]): The search result.
        """
        if search.description:
            items = items.filter(description__icontains=search.description)
        if search.price:
            items = items.filter(price=search.price)
        if search.price_is_gt:
            items = items.filter(price__gt=search.price_is_gt)
        if search.price_is_lt:
            items = items.filter(price__lt=search.price_is_lt)
        if search.created_on:
            items = items.filter(created_at__date=search.created_on)
        if search.created_after:
            items = items.filter(created_at__date__gt=search.created_after)
        if search.created_before:
            items = items.filter(created_at__date__lt=search.created_before)
        if search.updated_on:
            items = items.filter(updated_at__date=search.updated_on)
        if search.updated_after:
            items = items.filter(updated_at__date__gt=search.updated_after)
        if search.updated_before:
            items = items.filter(updated_at__date__lt=search.updated_before)
        if search.ids:
            items = items.filter(id__in=search.ids)
        if search.stores:
            items = items.filter(store__in=search.stores)

        return items

    def __filter(
        self,
        name: str | None = None,
        store: int | None = None,
        user: Any | None = None,
        search: ItemSearchSchema | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> QuerySet[Item]:
        """
        Filter items and order them by the updated date unless otherwise specified.

        Returns a QuerySet of items that match the provided filters.

        Args:
            name (str | None): The name of the item.
            store (int | None): The store where the item is stocked.
            user (User | AbstractBaseUser | AnonymousUser | None): The user who created the item.
            search (ItemSearchSchema): The search object for advanced filtering/searching.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            list[Item]: The filtered items.
        """
        items = Item.objects.select_related("user", "store").all()

        if name:
            items = items.filter(name__icontains=name)
        if store:
            items = items.filter(store_id=store)
        if user:
            items = items.filter(user=user)
        if search:
            items = self.__search(items=items, search=search)

        sort_field = sort or "updated_at"
        prefix = "" if sort_dir == "asc" else "-"
        items = items.order_by(f"{prefix}{sort_field}")

        return items

    async def __paginate(
        self,
        page_number: int = 1,
        items_per_page: int = 10,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
        store: int | None = None,
        name: str | None = None,
        search: ItemSearchSchema | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> ItemPaginationSchema:
        """
        Paginate the items.

        Returns a pagination schema with the items.

        Args:
            page_number (int): The page number.
            items_per_page (int): The number of items per page.
            user (User): The user to filter off.
            store (Store): Specific store to filter off.
            stores (list[Store]): The stores to filter off.
            name (int): The full or partial name of the item to filter by.
            search (ItemSearchSchema): The search object for advanced filtering/searching.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            ItemPaginationSchema: The paginated items.
        """
        records = self.__filter(
            user=user,
            store=store,
            name=name,
            search=search,
            sort=sort,
            sort_dir=sort_dir,
        )

        total = await records.acount()
        total_pages = ceil(total / items_per_page)
        total_pages = 1 if total_pages == 0 else total_pages

        start = (page_number - 1) * items_per_page
        end = start + items_per_page

        if start >= total:
            page_number = total_pages
            start = (page_number - 1) * items_per_page
            end = start + items_per_page

        paginated_items = records[start:end]
        items = [ItemSchema.from_orm(item) async for item in paginated_items]

        has_previous = page_number > 1
        previous_page = page_number - 1 if page_number > 1 else None
        has_next = end < total
        next_page = page_number + 1 if end < total else None

        return ItemPaginationSchema(
            items=items,
            total=total,
            page_number=page_number,
            total_pages=total_pages,
            has_previous=has_previous,
            previous_page=previous_page,
            has_next=has_next,
            next_page=next_page,
        )

    async def create_item(
        self,
        user: User | AbstractBaseUser | AnonymousUser,
        store_id: int,
        name: str,
        price: float,
        description: str = "",
    ) -> Item:
        """
        Create a shopping item.

        Args:
            user (User): The user that created the item.
            store_id (int): The store where the item is stocked.
            name (str): The item name.
            price (float): The price of the item.
            description (str): The item description.

        Returns:
            Item: The created item.
        """
        return await Item.objects.acreate(
            name=name,
            description=description,
            price=price,
            store_id=store_id,
            user=user,  # type: ignore
        )

    async def get_items(
        self,
        page: int = 1,
        items_per_page: int = 10,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
        store: int | None = None,
        name: str | None = None,
        search: ItemSearchSchema | None = None,
        sort: Literal["name", "created_on", "updated_on", "price"] | None = None,
        sort_dir: Literal["asc", "desc"] | None = None,
    ) -> ItemPaginationSchema:
        """
        Get all the items.

        Args:
            page (int): The page number.
            items_per_page (int): The number of items per page.
            user (User): The user to filter off.
            store (Store): Specific store to filter off.
            name (int): The full or partial name of the item to filter by.
            search (ItemSearchSchema): The search object for advanced filtering/searching.
            sort (str): The field to sort by.
            sort_dir (str): The direction to sort in.

        Returns:
            ItemPaginationSchema: The paginated items.
        """
        return await self.__paginate(
            page_number=page,
            items_per_page=items_per_page,
            user=user,
            store=store,
            search=search,
            name=name,
            sort=sort,
            sort_dir=sort_dir,
        )

    async def get_item(self, item_id: int) -> Item:
        """
        Get an item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Item: The item.
        """
        return await Item.objects.select_related("store", "user").aget(id=item_id)

    async def get_item_for_user(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> Item:
        """
        Get an item by its ID.

        Args:
            item_id (int): The ID of the item.

        Returns:
            Item: The item.
        """
        return await Item.objects.select_related("store", "user").aget(id=item_id, user=user)

    async def update_item(
        self,
        item: Item,
        name: str | None = None,
        price: float | None = None,
        description: str | None = None,
        store: int | None = None,
    ) -> Item:
        """
        Update an item.

        Args:
            item (Item): The item to update.
            name (str | None): The new name of the item.
            price (float | None): The new price of the item.
            description (str | None): The new description of the item.
            store (int | None): The new store for the item.

        Returns:
            Item: The updated item.
        """
        if name:
            item.name = name
        if price:
            item.price = price
        if description:
            item.description = description
        if store:
            item.store_id = store

        await item.asave()
        return item

    async def delete_item(
        self,
        item_id: int,
        user: User | AbstractBaseUser | AnonymousUser,
    ) -> None:
        """
        Delete an item by its ID.

        Args:
            item_id (int): The ID of the item.
            user (User | AnonymousUser | AbstractBaseUser): The user who created the item.

        Raises:
            Item.DoesNotExist: If the item does not exist.
        """
        item = await Item.objects.aget(id=item_id, user=user)
        await item.adelete()

    @no_type_check
    async def aggregate(
        self,
        user: User | AbstractBaseUser | AnonymousUser | None = None,
    ) -> dict[str, Any]:
        """
        Aggregate the items.

        Returns:
            dict[str, Any]: The aggregation of the items.
        """
        items = self.__filter(user=user)

        return await items.aaggregate(
            total_items=Count("id"),
            total_price=Sum("price"),
            average_price=Avg("price"),
            max_price=Max("price"),
            min_price=Min("price"),
        )

    async def does_item_exist(
        self,
        name: str,
        store_id: int | None = None,
    ) -> bool:
        """
        Check if a item exists with the provided details.

        Args:
            name (str): The name of the item.
            store_id (int): The store we are checking against.

        Returns:
            bool: True if the item exists, false otherwise.
        """
        items = Item.objects.filter(name=name)
        if store_id:
            items = items.filter(store_id=store_id)
        return await items.aexists()
