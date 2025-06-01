"""Contains factories for the items app."""

from uuid import uuid4

from factory import Sequence, SubFactory  # type: ignore
from factory.django import DjangoModelFactory
from faker import Faker

from authentication.tests.factory import UserFactory
from items.models import ShoppingItem as Item
from stores.tests.factory import StoreFactory

faker = Faker()


class ItemFactory(DjangoModelFactory[Item]):
    """Factory for the User model."""

    class Meta:
        """Meta class."""

        model = Item

    name = Sequence(lambda n: f"{faker.word()} Item {n}-{uuid4().hex}")  # type: ignore
    description = faker.sentence()
    price = faker.random_number(digits=2)
    store = SubFactory(StoreFactory)  # type: ignore
    user = SubFactory(UserFactory)  # type: ignore
