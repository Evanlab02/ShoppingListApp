"""Contains the config loaders for the benchmarking tool."""

import json

from schemas import LoginInput


def load_config(path: str) -> dict:  # type: ignore
    """Load a config from a file."""
    with open(path, "r") as f:
        return json.load(f)  # type: ignore


def load_login_config() -> LoginInput:
    """Load the login config."""
    return LoginInput(**load_config("config/login.json"))
