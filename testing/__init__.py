"""Load testing for auth endpoints."""

from random import randint
from uuid import uuid4
from locust import FastHttpUser, task, tag

KEY = "319d79eed1d94708adb4f4c6e71eaea4"


class TestCase(FastHttpUser):
    """Test the API."""

    def on_start(self):
        """On test user start up."""
        self.client.post(
            "/api/v1/auth/login",
            json={"username": "AnimalAlpaca", "password": "devadmin"},
            headers={
                "Content-Type": "application/json"
            }
        )

    def on_stop(self):
        """On user close."""
        self.client.post(
            "/api/v1/auth/logout",
            headers={
                "Content-Type": "application/json"
            }
        )

    @task
    @tag("auth")
    def register_login_logout(self):
        """Register random generated user, login and then logout."""
        random_id = uuid4().hex
        self.client.post(
            "/api/v1/auth/register",
            json={
                "username": f"{random_id}",
                "password": f"{random_id}",
                "password_confirmation": f"{random_id}",
                "first_name": f"{random_id}",
                "last_name": f"{random_id}",
                "email": f"{random_id}@gmail.com"
            },
            headers={
                "Content-Type": "application/json"
            }
        )

        self.client.post(
            "/api/v1/auth/login",
            json={
                "username": f"{random_id}",
                "password": f"{random_id}",
            },
            headers={
                "Content-Type": "application/json"
            }
        )

        self.client.post(
            "/api/v1/auth/logout",
            headers={
                "Content-Type": "application/json"
            }
        )

    @task
    @tag("api")
    def types_mapping(self):
        """Get store types mapping."""
        self.client.get(
            "/api/v1/stores/types/mapping",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": KEY
            }
        )

    @task
    @tag("api")
    def create_store_and_detail_store(self):
        """Create store and get details."""
        random_id = uuid4().hex
        random_store_type = randint(1, 3)
        response = self.client.post(
            "/api/v1/stores/create",
            json={
                "name": f"{random_id}",
                "store_type": random_store_type,
                "description": f"{random_id}"
            },
            headers={
                "Content-Type": "application/json",
                "X-API-Key": KEY
            }
        )

        data = response.json()
        store_id = data.get("id", 1)

        self.client.get(
            f"/api/v1/stores/detail/{store_id}",
            name="/api/v1/stores/detail/id",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": KEY
            }
        )

    @task
    @tag("web")
    def create_store_and_detail_store_web(self):
        """Create store and get details."""
        self.client.get(
            "/stores/",
            headers={
                "X-API-Key": KEY
            }
        )

    @task
    @tag("api")
    def get_stores(self):
        """Get stores."""
        data = {"has_next": True}
        page = 0
        while data.get("has_next", False):
            page += 1
            response = self.client.get(
                f"/api/v1/stores?limit=10&page={page}",
                name="/api/v1/stores",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": KEY
                }
            )
            data = response.json()

        data = {"has_next": True}
        page = 0
        while data.get("has_next", False):
            page += 1
            response = self.client.get(
                f"/api/v1/stores/me?limit=10&page={page}",
                name="/api/v1/stores/me",
                headers={
                    "Content-Type": "application/json",
                    "X-API-Key": KEY
                }
            )
            data = response.json()

    @task
    @tag("api")
    def get_aggregations(self):
        """Aggregations."""
        self.client.get(
            "/api/v1/stores/aggregate",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": KEY
            }
        )

        self.client.get(
            "/api/v1/stores/aggregate/me",
            headers={
                "Content-Type": "application/json",
                "X-API-Key": KEY
            }
        )
