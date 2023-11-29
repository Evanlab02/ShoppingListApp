"""Contains the models for the authentication app."""

from uuid import uuid4

from django.contrib.auth.models import User
from django.db.models import CASCADE, CharField, DateTimeField, Model, OneToOneField
from django.utils import timezone
from django.utils.timezone import timedelta  # type: ignore


class Client(Model):
    """
    Model for a client, a wrapper around a user.

    Attributes:
        user (User): The user that the client is wrapping.
        token (str): The token for the client.
        token_expiration (datetime): The expiration date of the token.

    Methods:
        __str__: Returns the string representation of the client.
        generate_token: Generates a token for the client.
    """

    user = OneToOneField(User, on_delete=CASCADE)
    token = CharField(max_length=100, blank=True)
    token_expiration = DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        """Return the string representation of the client."""
        return f"{self.user.username} ({self.user.email})"

    def generate_token(self) -> None:
        """Generate a token for the client."""
        if self.token_expiration is None or self.token_expiration < timezone.now():
            self.token = uuid4().hex
            self.token_expiration = timezone.now() + timedelta(days=1)
            self.save()
