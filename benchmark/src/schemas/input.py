"""Contains the input schemas for the benchmarking tool."""

from pydantic import BaseModel


class RegisterInput(BaseModel):
    """Input schema for the register endpoint."""

    username: str
    password: str
    password_confirmation: str
    email: str
    first_name: str
    last_name: str


class LoginInput(BaseModel):
    """Input schema for the login endpoint."""

    username: str
    password: str
