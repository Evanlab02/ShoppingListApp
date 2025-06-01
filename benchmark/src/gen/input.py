"""Contains the factory boy factories for the input schemas."""

from uuid import uuid4

import factory
from factory.base import Factory
from faker import Faker

from schemas import RegisterInput

fake = Faker()


class RegisterInputFactory(Factory[RegisterInput]):
    """Factory for the RegisterInput schema."""

    class Meta:
        """Meta class for the RegisterInputFactory."""

        model = RegisterInput

    username = factory.LazyAttribute(lambda o: f"{uuid4().hex}{fake.user_name()}")  # type: ignore
    email = factory.LazyAttribute(lambda o: f"{uuid4().hex}{fake.email()}")  # type: ignore
    first_name = factory.Faker("first_name")  # type: ignore
    last_name = factory.Faker("last_name")  # type: ignore
    password = factory.Faker("password")  # type: ignore
    password_confirmation = factory.SelfAttribute("password")  # type: ignore
