"""Contains the auth locust user definitions."""

from locust import FastHttpUser, between, tag, task

from clients import AuthClient
from config import USER_LOGIN
from gen import RegisterInputFactory


class AuthUser(FastHttpUser):
    """Auth locust user."""

    wait_time = between(1, 5)  # type: ignore
    weight = 1
    network_timeout = 5
    connection_timeout = 5

    def __init__(self, environment) -> None:  # type: ignore
        """Initialize the auth user."""
        super().__init__(environment)
        self.iclient = AuthClient(self.client)

    @tag("1")
    @task(weight=1)
    def register(self) -> None:
        """Register a new user."""
        self.iclient.register(RegisterInputFactory.create())

    @tag("2")
    @task(weight=100)
    def login(self) -> None:
        """Login a user."""
        self.iclient.login(USER_LOGIN, clear=True)

    @tag("3")
    @task(weight=10)
    def logout(self) -> None:
        """Logout a user."""
        self.iclient.logout(do_login=True, payload=USER_LOGIN)
