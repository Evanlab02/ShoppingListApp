"""Contains the forms for items."""

from typing import Any

from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.forms import ModelForm

from items.database import IItemRepo, ItemRepo
from items.models import ShoppingItem as Item
from stores.database import IStoreRepo, StoreRepo
from stores.models import ShoppingStore as Store


class ItemForm(ModelForm):  # type: ignore
    """Form for creating and updating items."""

    class Meta:
        """Meta class for the ItemForm."""

        model = Item
        fields = ["name", "store", "price", "description"]

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the ItemForm.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        # Repositories
        self.repo: IItemRepo = ItemRepo()
        self.store_repo: IStoreRepo = StoreRepo()

        # Styles
        self.input_style = "input input-bordered w-full focus:border-[#602786] focus:outline-none"
        self.select_style = (
            "select select-bordered w-full focus:border-[#602786] focus:outline-none"
        )

        # User
        self.user: User = kwargs.pop("user")

        # Instance
        self.instance: Item | None = kwargs.get("instance")
        if self.instance and self.instance.user != self.user:
            raise PermissionDenied("You are not allowed to update this item.")

        super().__init__(*args, **kwargs)
        self.fields["store"].queryset = Store.objects.all()  # type: ignore

        # Style all inputs
        self.fields["name"].widget.attrs["class"] = self.input_style
        self.fields["store"].widget.attrs["class"] = self.select_style
        self.fields["price"].widget.attrs["class"] = self.input_style
        self.fields["description"].widget.attrs["class"] = self.input_style

        # Synchronous functions
        self.does_item_exist = async_to_sync(self.repo.does_item_exist)
        self.does_store_exist = async_to_sync(self.store_repo.does_store_exist)

    def clean(self) -> dict[str, Any] | None:
        """
        Clean the form data.

        Returns:
            dict[str, Any] | None: The cleaned data.
        """
        cleaned_data = super().clean()
        name: str = cleaned_data.get("name")  # type: ignore
        store: Store | None = cleaned_data.get("store")  # type: ignore

        if not store:
            self.add_error("store", "Store does not exist.")
        elif self.does_item_exist(name=name, store_id=store.id):
            self.add_error("name", "Item with this name already exists in this store.")

        return cleaned_data

    def save(self, commit: bool = True) -> Item:
        """
        Save the form data.

        Returns:
            Item: The saved item.
        """
        self.instance.user = self.user  # type: ignore
        return super().save(commit=commit)  # type: ignore
