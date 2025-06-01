"""Contains the auth client for the benchmarking tool."""

from locust.contrib.fasthttp import FastHttpSession

from schemas import LoginInput, RegisterInput


class AuthClient:
    """Client for the auth endpoints and views."""

    def __init__(self, session: FastHttpSession):
        """Initialize the auth client."""
        self.session = session
        self.base_api = "/api/v1/auth"

    def register(self, payload: RegisterInput) -> None:
        """
        Register a new user.

        Args:
            payload: The payload to register the user with.
        """
        self.session.post(f"{self.base_api}/register", json=payload.model_dump())

    def login(self, payload: LoginInput, clear: bool = False) -> None:
        """
        Login a user.

        Args:
            payload: The payload to login the user with.
        """
        self.session.post(f"{self.base_api}/login", json=payload.model_dump())
        if clear:
            self.session.cookiejar.clear()

    def logout(self, do_login: bool = False, payload: LoginInput | None = None) -> None:
        """Logout a user."""
        if do_login and payload:
            self.login(payload, clear=False)

        self.session.post(f"{self.base_api}/logout")
