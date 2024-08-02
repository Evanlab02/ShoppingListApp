"""Contains the populate command."""

import logging
from typing import no_type_check

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from items.models import ShoppingItem as Item
from stores.models import ShoppingStore as Store

log = logging.getLogger(__name__)
log.info("Loading django populate command...")


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

        for i in range(1, 101):
            item = Item.objects.create(
                name=f"Item {i}",
                description=f"Description {i}",
                price=i * 100,
                store=store,
                user=user,
            )
            item.save()


log.info("Loaded django populate command.")
