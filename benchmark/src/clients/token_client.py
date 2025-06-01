"""Contains the token client for the benchmarking tool."""

from locust.contrib.fasthttp import FastHttpSession

from schemas import TokenOutput


class TokenClient:
    """Client for the token endpoints and views."""

    def __init__(self, session: FastHttpSession):
        """Initialize the token client."""
        self.session = session
        self.base_api = "/api/v1/token"

    def get(self) -> TokenOutput:
        """
        Get a token for a user.

        Args:
            payload: The payload to get a token for.
        """
        response = self.session.get(self.base_api)
        return TokenOutput(**response.json())
