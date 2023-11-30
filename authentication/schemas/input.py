"""Contains the input schemas for the authentication app."""

from ninja import Schema


class NewUser(Schema):
    """The schema for a new user."""

    username: str
    password: str
    password_confirmation: str
    first_name: str
    last_name: str
    email: str
