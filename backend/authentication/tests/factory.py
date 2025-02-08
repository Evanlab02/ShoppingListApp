"""Contains factories for the authentication app."""

from django.contrib.auth.models import User
from factory import Factory, SubFactory  # type: ignore
from factory.django import DjangoModelFactory, Password
from faker import Faker

from authentication.models import ApiClient
from authentication.schemas.input import NewUser

faker = Faker()


class UserFactory(DjangoModelFactory[User]):
    """Factory for the User model."""

    class Meta:
        """Meta class."""

        model = User

    username = faker.user_name()
    email = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()
    password = Password("test")  # type: ignore


class ClientFactory(DjangoModelFactory[ApiClient]):
    """Factory for the Client model."""

    class Meta:
        """Meta class."""

        model = ApiClient

    user = SubFactory(UserFactory)  # type: ignore
    is_active = True
    client_secret = None
    token = None
    token_expiration = 0


class NewUserSchemaFactory(Factory[NewUser]):
    """Factory for the NewUserSchema model."""

    class Meta:
        """Meta class."""

        model = NewUser

    username = faker.user_name()
    password = "test"
    password_confirmation = "test"
    first_name = faker.first_name()
    last_name = faker.last_name()
    email = faker.email()
