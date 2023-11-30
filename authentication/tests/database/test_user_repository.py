"""Contains tests for the database module."""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase

from authentication.database.user_repository import is_user_authenticated

from ..helpers import create_test_user


class TestUserRepository(TestCase):
    """Test the UserRepository class."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.client = Client()
        return super().setUp()

    def test_user_is_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        self.client.force_login(self.user)
        is_authenticated = is_user_authenticated(self.user)
        assert is_authenticated is True

    def test_user_is_not_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        user = AnonymousUser()
        is_authenticated = is_user_authenticated(user)
        assert is_authenticated is False
