"""Load testing for auth endpoints."""

from uuid import uuid4

from locust import FastHttpUser, tag, task
from faker import Faker
from time import sleep

faker = Faker()

class TestCase(FastHttpUser):
    """Test the API."""

    def on_start(self):
        """On test user start up."""
        self.client.post(
            "/api/v1/auth/login",
            json={"username": "AnimalAlpaca", "password": "devadmin"},
            headers={"Content-Type": "application/json"},
        )

    def on_stop(self):
        """On user close."""
        self.client.post(
            "/api/v1/auth/logout", headers={"Content-Type": "application/json"}
        )

    @tag("write")
    @tag("store")
    @tag("store_create")
    @task
    def create_store(self):
        """Create a store."""
        self.client.post(
            "/api/v1/stores/create",
            json={
                "name": faker.company() + uuid4().hex,
                "store_type": faker.random_element(elements=[1, 2, 3]),
                "description": faker.sentence()
            },
            headers={"Content-Type": "application/json"},
        )
        sleep(1)
