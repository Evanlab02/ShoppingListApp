"""Load testing for auth endpoints."""

import os
from datetime import datetime, timedelta
from time import sleep
from uuid import uuid4

import jwt
from faker import Faker
from locust import FastHttpUser, tag, task

faker = Faker()
TOKEN_HEADER = "X-API-Token"


class TestCase(FastHttpUser):
    """Test the API."""

    host = "http://shopping-django-site:80"

    def __init__(self, environment) -> None:
        super().__init__(environment)
        self.token = None
        self.token_expiry = None

    def on_start(self) -> None:
        """On test user start up."""
        username = faker.user_name() + uuid4().hex
        password = faker.password()
        response = self.client.post(
            "/api/v1/auth/register",
            json={
                "username": username,
                "password": password,
                "password_confirmation": password,
                "first_name": faker.first_name(),
                "last_name": faker.last_name(),
                "email": uuid4().hex + faker.email(),
            },
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 201:
            raise Exception(f"Failed to register user: {response.text}")

        login_response = self.client.post(
            "/api/v1/auth/login",
            json={"username": username, "password": password},
            headers={"Content-Type": "application/json"},
        )

        if login_response.status_code != 200:
            raise Exception(f"Failed to login user: {login_response.text}")

    def on_stop(self) -> None:
        """On user close."""
        self.client.post("/api/v1/auth/logout", headers={"Content-Type": "application/json"})

    def get_token(self) -> str:
        """Get the token for the user."""
        if (
            self.token is None
            or self.token_expiry is None
            or (self.token_expiry - timedelta(minutes=1)) <= datetime.now()
        ):
            response = self.client.get(
                "/api/v1/token",
                headers={"Content-Type": "application/json"},
            )
            token = response.json()["token"]
            secret = response.json()["secret"]

            self.token = token
            self.token_expiry = datetime.fromtimestamp(
                jwt.decode(token, secret, algorithms=["HS256"])["exp"]
            )
            sleep(1)

        return self.token

    @tag("api")
    @tag("api_store_create")
    @task
    def create_store(self) -> None:
        """Create a store via the API."""
        token = self.get_token()
        self.client.post(
            "/api/v1/stores/create",
            json={
                "name": faker.company() + uuid4().hex,
                "store_type": faker.random_element(elements=[1, 2, 3]),
                "description": faker.sentence(),
            },
            headers={"Content-Type": "application/json", TOKEN_HEADER: token},
        )
        sleep(1)
