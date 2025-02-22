"""Factory for the stores app."""

from uuid import uuid4

from factory import Sequence, SubFactory  # type: ignore
from factory.django import DjangoModelFactory
from faker import Faker

from authentication.tests.factory import UserFactory
from stores.constants import STORE_TYPE_CHOICES
from stores.models import ShoppingStore as Store

faker = Faker()


class StoreFactory(DjangoModelFactory[Store]):
    """Factory for the Store model."""

    class Meta:
        """Meta class."""

        model = Store

    name = Sequence(lambda n: f"{faker.word()} Store {n}-{uuid4().hex}")  # type: ignore
    store_type = faker.random_element([choice[0] for choice in STORE_TYPE_CHOICES])
    description = faker.sentence()
    user = SubFactory(UserFactory)  # type: ignore
