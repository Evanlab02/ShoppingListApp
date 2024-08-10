"""Contains api exceptions for the authentication app."""

import logging

log = logging.getLogger(__name__)
log.info("Loading auth API exceptions...")


class UserAlreadyLoggedIn(Exception):
    """Exception raised when a user is already logged in."""

    def __init__(self) -> None:
        """Exception raised when a user is already logged in."""
        super().__init__("User is already logged in.")


class UsernameAlreadyExists(Exception):
    """Exception raised when a username already exists."""

    def __init__(self) -> None:
        """Exception raised when a username already exists."""
        super().__init__("Username already exists.")


class EmailAlreadyExists(Exception):
    """Exception raised when a email already exists."""

    def __init__(self) -> None:
        """Exception raised when a email already exists."""
        super().__init__("Email already exists.")


class InvalidUserDetails(Exception):
    """Exception raised when a payload is invalid."""

    def __init__(self) -> None:
        """Exception raised when a payload is invalid."""
        super().__init__("Please ensure username, email, first name and last name are provided.")


class NonMatchingCredentials(Exception):
    """Exception raised when a password and password confirmation do not match."""

    def __init__(self) -> None:
        """Exception raised when a password and password confirmation do not match."""
        super().__init__("Password and password confirmation do not match.")


class InvalidCredentials(Exception):
    """Exception raised when a password or username is invalid."""

    def __init__(self) -> None:
        """Exception raised when a password or username is invalid."""
        super().__init__("Invalid Credentials.")


class UserNotLoggedIn(Exception):
    """Exception raised when a user is not logged in."""

    def __init__(self) -> None:
        """Exception raised when a user is not logged in."""
        super().__init__("User is not logged in.")


class ApiClientAlreadyRegistered(Exception):
    """Exception raised when a user has already registered an api client."""

    def __init__(self) -> None:
        """Exception raised when a user has already registered an api client."""
        super().__init__("Api Client is already registered.")


log.info("Loaded auth API exceptions.")
