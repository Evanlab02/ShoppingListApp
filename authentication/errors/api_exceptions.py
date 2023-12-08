"""Contains api exceptions for the authentication app."""

import logging


class UserAlreadyLoggedIn(Exception):
    """Exception raised when a user is already logged in."""

    def __init__(self) -> None:
        """Exception raised when a user is already logged in."""
        logging.warning("User was already logged in.")
        super().__init__("User is already logged in.")


class UsernameAlreadyExists(Exception):
    """Exception raised when a username already exists."""

    def __init__(self) -> None:
        """Exception raised when a username already exists."""
        logging.warning("Received username that already exists.")
        super().__init__("Username already exists.")


class EmailAlreadyExists(Exception):
    """Exception raised when a email already exists."""

    def __init__(self) -> None:
        """Exception raised when a email already exists."""
        logging.warning("Received email that already exists.")
        super().__init__("Email already exists.")


class InvalidUserDetails(Exception):
    """Exception raised when a payload is invalid."""

    def __init__(self) -> None:
        """Exception raised when a payload is invalid."""
        logging.warning("Received invalid user details.")
        super().__init__(
            "Please ensure username, email, first name and last name are provided."
        )


class NonMatchingCredentials(Exception):
    """Exception raised when a password and password confirmation do not match."""

    def __init__(self) -> None:
        """Exception raised when a password and password confirmation do not match."""
        logging.warning("Received non-matching credentials.")
        super().__init__("Password and password confirmation do not match.")


class InvalidCredentials(Exception):
    """Exception raised when a password or username is invalid."""

    def __init__(self) -> None:
        """Exception raised when a password or username is invalid."""
        logging.warning("Received invalid credentials.")
        super().__init__("Invalid Credentials.")


class UserNotLoggedIn(Exception):
    """Exception raised when a user is not logged in."""

    def __init__(self) -> None:
        """Exception raised when a user is not logged in."""
        logging.warning("User was not logged in.")
        super().__init__("User is not logged in.")
