"""Contains test helpers for the authentication app."""

from django.contrib.auth.models import User


def create_test_user() -> User:
    """Create a test user."""
    user = User.objects.create_user(
        username="test",
        password="test",
        email="test@gmail.com",
    )
    user.save()
    return user
