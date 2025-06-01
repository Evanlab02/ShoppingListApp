"""Contains the output schemas for the benchmarking tool."""

from pydantic import BaseModel


class TokenOutput(BaseModel):
    """Output schema for the token endpoint."""

    token: str
    secret: str
