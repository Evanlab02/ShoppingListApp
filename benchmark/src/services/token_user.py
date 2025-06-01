"""Contains the token locust user definitions."""

from locust import FastHttpUser, between, tag, task

from clients import AuthClient, TokenClient
from config import USER_LOGIN


class TokenUser(FastHttpUser):
    """Token locust user."""

    wait_time = between(1, 5)  # type: ignore
    weight = 5
    network_timeout = 5
    connection_timeout = 5

    def __init__(self, environment) -> None:  # type: ignore
        """Initialize the token user."""
        super().__init__(environment)
        self.auth_client = AuthClient(self.client)
        self.iclient = TokenClient(self.client)

    def on_start(self) -> None:
        """On start of the token user."""
        self.auth_client.login(USER_LOGIN)
        return super().on_start()

    def on_stop(self) -> None:
        """On stop of the token user."""
        self.auth_client.logout()
        return super().on_stop()  # type: ignore

    @tag("4")
    @task(weight=1)
    def get_token(self) -> None:
        """Get a token for a user."""
        self.iclient.get()
