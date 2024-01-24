"""Contains the populate command."""

from typing import no_type_check

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from stores.models import ShoppingStore as Store


class Command(BaseCommand):
    """Populate the database with dummy data."""

    help = "Populate the database with dummy data."

    @no_type_check
    def handle(self, *args, **options) -> None:
        """Handle the command."""
        # Create a test user
        user = User.objects.create_user(
            username="basetestuser1",
            email="testuser@gmail.com",
            password="testuser",
            first_name="Test",
            last_name="User",
        )
        user.save()

        other_user = User.objects.create_user(
            username="basetestuser2",
            email="testuser2@gmail.com",
            password="testuser2",
            first_name="Tester",
            last_name="User",
        )
        other_user.save()

        # Create a store
        store = Store.objects.create(
            name="Base Test Store",
            store_type=3,
            description="This is a test store.",
            user=user,
        )
        store.save()
