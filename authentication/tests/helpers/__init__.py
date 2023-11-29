"""Contains test helpers for the authentication app."""

from django.contrib.auth.models import User

from authentication.models import Client as UserClient


def create_test_user():
    """Create a test user."""
    user = User.objects.create_user(
        username="test",
        password="test",
        email="test@gmail.com",
    )
    user.save()
    return user


def create_test_user_client(user: User):
    """Create a test user client."""
    client = UserClient(user=user)
    client.save()
    return client
