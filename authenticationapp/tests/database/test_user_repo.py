"""Contains tests for the user repository."""

import pytest

from authenticationapp.database import UserRepository

from ..helpers import DjangoClient, TestCase, create_test_user, create_test_user_client


class TestUserRepo(TestCase):
    """Test the User repository."""

    @pytest.mark.django_db(transaction=True)
    def setUp(self) -> None:
        """Set up the tests."""
        self.django_client = DjangoClient()
        self.user_repo = UserRepository()
        self.user = create_test_user()
        self.user_client = create_test_user_client(self.user)
        return super().setUp()

    def test_is_authenticated(self):
        """Test the is_authenticated method."""
        self.django_client.force_login(self.user)
        assert self.user_repo.is_authenticated(self.user) is True

    def test_create_user_with_non_matching_passwords(self):
        """Test the create_user method with invalid passwords."""
        username = "test_username"
        password = "test_password"
        confirm_password = "test_pa"
        email = "test_email"
        first_name = "test_first_name"
        last_name = "test_last_name"

        with pytest.raises(ValueError):
            self.user_repo.create_user(
                username=username,
                password=password,
                password_confirmation=confirm_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

    def test_create_user_with_existing_username(self):
        """Test the create_user method with an existing username."""
        username = self.user.username
        password = "test_password"
        confirm_password = "test_password"
        email = "test_email"
        first_name = "test_first_name"
        last_name = "test_last_name"

        with pytest.raises(ValueError):
            self.user_repo.create_user(
                username=username,
                password=password,
                password_confirmation=confirm_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

    def test_create_user_with_existing_email(self):
        """Test the create_user method with an existing email."""
        username = "test_username"
        password = "test_password"
        confirm_password = "test_password"
        email = self.user.email
        first_name = "test_first_name"
        last_name = "test_last_name"

        with pytest.raises(ValueError):
            self.user_repo.create_user(
                username=username,
                password=password,
                password_confirmation=confirm_password,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

    def test_create_user(self):
        """Test the create_user method."""
        username = "test_username"
        email = "test_email"
        password = "test_password"
        password_confirmation = "test_password"
        first_name = "test_first_name"
        last_name = "test_last_name"

        user = self.user_repo.create_user(
            username=username,
            email=email,
            password=password,
            password_confirmation=password_confirmation,
            first_name=first_name,
            last_name=last_name,
        )

        assert user.username == username
        assert user.email == email
        assert user.first_name == first_name
        assert user.last_name == last_name
