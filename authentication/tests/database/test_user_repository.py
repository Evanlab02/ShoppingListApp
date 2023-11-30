"""Contains tests for the database module."""

import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import Client, TestCase

from authentication.database.user_repository import (
    create_user,
    does_username_exist,
    is_user_authenticated,
)

from ..helpers import create_test_user


class TestUserRepository(TestCase):
    """Test the UserRepository class."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.user = create_test_user()
        self.client = Client()
        return super().setUp()

    async def test_create_user(self) -> None:
        """Test the create_user method."""
        username = "testcreate"
        password = "testcreate"
        email = "test@gmail.com"
        first_name = "test"
        last_name = "create"

        user = await create_user(username, password, first_name, last_name, email)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)

    def test_user_is_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        self.client.force_login(self.user)
        is_authenticated = is_user_authenticated(self.user)
        self.assertTrue(is_authenticated)

    def test_user_is_not_authenticated(self) -> None:
        """Test the is_user_authenticated method."""
        user = AnonymousUser()
        is_authenticated = is_user_authenticated(user)
        self.assertFalse(is_authenticated)

    async def test_username_exists(self) -> None:
        """Test the does_username_exist method."""
        username_exists = await does_username_exist(self.user.username)
        self.assertTrue(username_exists)

    async def test_username_does_not_exist(self) -> None:
        """Test the does_username_exist method."""
        username_exists = await does_username_exist("thisshouldnotexist")
        self.assertFalse(username_exists)
