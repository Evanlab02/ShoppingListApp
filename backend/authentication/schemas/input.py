"""Contains the input schemas for the authentication app."""

import logging

from ninja import Schema

log = logging.getLogger(__name__)
log.info("Loading authentication input schemas...")


class NewUser(Schema):
    """The schema for a new user."""

    username: str
    password: str
    password_confirmation: str
    first_name: str
    last_name: str
    email: str


class UserCredentials(Schema):
    """The schema for a user's details."""

    username: str
    password: str


log.info("Loaded authentication input schemas.")
